import functools
import os
from typing import Any, Optional, OrderedDict

from .state import State
import openapi_client as client
import click
from os import path
from .logger import log
from .auth import Authenticator
from .helpers import (
    load_config,
    parse_betas,
    validate_auth_method,
    validate_export_parameter,
    validate_person_mode_download_format,
    get_timestamp,
    get_measurements_dict,
    Uploader,
)
from .motions import Motion

from .scenes import Scene
from .user import request_user_info
from functools import partial
from .avatars import Avatar


CURRENT_DIR = path.dirname(path.abspath(__file__))
DEFAULT_CONFIG = path.join(CURRENT_DIR, "../configs/prod.toml")


class CustomOption(click.Option):
    """Custom option class that adds the attribute help_group to the option"""

    def __init__(self, *args, **kwargs):
        self.help_group = kwargs.pop("help_group", None)
        super().__init__(*args, **kwargs)


class CustomCommand(click.Command):
    """Custom command class that can be used to format the help text."""

    def format_options(self, ctx, formatter):
        """Writes options into the help text. Separates them by help_group"""
        opts = OrderedDict([("Options", [])])
        for param in self.get_params(ctx):
            rv = param.get_help_record(ctx)
            if rv is not None:
                if hasattr(param, "help_group"):
                    opts.setdefault(param.help_group, []).append(rv)
                else:
                    opts["Options"].append(rv)

        for help_group, param in opts.items():
            with formatter.section(help_group):
                formatter.write_dl(param)


def avatar_download_format(func):
    """Decorator to add avatar download format to a command."""

    @click.option(
        "--download-format",
        cls=CustomOption,
        help_group="Avatar download options",
        type=click.Choice(["OBJ", "FBX"], case_sensitive=False),
        is_eager=True,
        help="Format for downloading avatar.",
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def avatar_scene_download_format(func):
    """Decorator to add avatar and scene download format to a command."""

    @click.option(
        "--download-format",
        cls=CustomOption,
        help_group="Avatar download options",
        type=click.Choice(["OBJ", "FBX", "GLB"], case_sensitive=False),
        is_eager=True,
        help="Format for downloading avatar or scene. GLB is only applicable to multi-avatar/scene mode.",
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def avatar_download_params(func):
    """Decorator to add avatar download options to a command."""

    @click.option(
        "--pose",
        cls=CustomOption,
        help_group="Avatar download options",
        type=click.Choice(["T", "A", "I", "SCAN"], case_sensitive=False),
        callback=validate_export_parameter,
        help="""Pose the downloaded avatar should be in. SCAN is not applicable for avatars created from betas or 
        measurements since it corresponds to a captured pose or motion.""",
    )
    @click.option(
        "--animation",
        cls=CustomOption,
        help_group="Avatar download options",
        type=click.Choice(["a-salsa"], case_sensitive=False),
        callback=validate_export_parameter,
        help="Animation for the downloaded avatar",
    )
    @click.option(
        "--compatibility-mode",
        cls=CustomOption,
        help_group="Avatar download options",
        type=click.Choice(["DEFAULT", "OPTITEX", "UNREAL"], case_sensitive=False),
        callback=validate_export_parameter,
        help="Adjust output for compatibility with selected software.",
    )
    @click.option(
        "--out-file",
        cls=CustomOption,
        help_group="Avatar download options",
        type=click.Path(dir_okay=False),
        callback=validate_export_parameter,
        help="File to save created avatar mesh to",
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


@click.group()
@click.pass_context
@click.option(
    "--config",
    type=click.Path(exists=True),
    default=os.environ.get("MCME_CONFIG_PATH", DEFAULT_CONFIG),
    help="Path to config file",
)
@click.option(
    "--username",
    default=lambda: os.environ.get("MCME_USERNAME"),
    help="Username for authentication with Meshcapade.me. Alternatively, set env variable MCME_USERNAME.",
)
@click.option(
    "--password",
    default=lambda: os.environ.get("MCME_PASSWORD"),
    help="Password for authentication with Meshcapade.me. Alternatively, set env variable MCME_PASSWORD.",
)
@click.option(
    "--token",
    type=str,
    default=lambda: os.environ.get("MCME_TOKEN"),
    help="Authentication token retrieved from Meshcapade.me. Alternatively, set env variable MCME_TOKEN. "
    "Please don't set username and password when setting a token.",
)
def cli(ctx: click.Context, username: str, password: str, config: str, token: str) -> None:
    """
    Command-line interface for the Meshcapade.me API.
    """
    ctx.ensure_object(dict)
    ctx.obj["config"] = load_config(config)
    ctx.obj["keycloak_token_file"] = os.path.expanduser(ctx.obj["config"]["cli_state"]["keycloak_token_file"])
    validate_auth_method(username, password, token)
    ctx.obj["username"] = username
    ctx.obj["password"] = password
    ctx.obj["token"] = token
    # construct api client
    configuration = client.Configuration(host=ctx.obj["config"]["api"]["host"])
    ctx.obj["api_client"] = client.ApiClient(configuration)


def require_auth(func):
    """Decorator to authenticate with the meshcapade.me API. Only required for commands making API calls."""

    @functools.wraps(func)
    @click.pass_context
    def wrapper(ctx: click.Context, *args, **kwargs):
        authenticator = Authenticator(auth_config=ctx.obj["config"]["auth"])
        state = State(ctx.obj["keycloak_token_file"])
        username = ctx.obj["username"]
        password = ctx.obj["password"]
        token = ctx.obj["token"]
        api_client = ctx.obj["api_client"]
        if username:
            state.active_user = username
        if token is not None:
            log.debug("Used token provided by user")
            username = authenticator.get_user_from_token(token=token)  # raises an error if token is invalid
            state.active_user = username
            state.set_active_keycloak_token(token)
            api_client.configuration.access_token = token
        elif (token := state.active_access_token) is not None and authenticator.is_access_token_valid(token):
            log.debug("Used saved auth token.")
            api_client.configuration.access_token = token
        else:
            log.debug("Authenticated with username and password.")
            keycloak_token = authenticator.authenticate(username, password)
            state.set_active_keycloak_token(keycloak_token)
            api_client.configuration.access_token = state.active_access_token
        return func(*args, **kwargs)

    return wrapper


@cli.result_callback()
@click.pass_context
def close_api_client(ctx: click.Context, result: Any, **kwargs):
    """Cleanup function that closes the api client."""
    ctx.obj["api_client"].close()


@cli.group()
@click.pass_context
@require_auth
def create(ctx: click.Context) -> None:
    """
    Create avatars or scenes. Please be aware that these commands cost credits.
    """
    # all create avatar operations need keycloak authentication


@create.command(cls=CustomCommand, name="from-betas")
@click.pass_context
@click.option(
    "--gender",
    type=click.Choice(client.EnumsGender.enum_values(), case_sensitive=False),
    help="Gender of created avatar",
)
@click.option(
    "--betas",
    type=click.UNPROCESSED,
    callback=partial(parse_betas, is_smplx=False),
    help='Beta values. Supply like 0.1,0.2 or "[0.1,0.2]"',
)
@click.option("--name", type=str, default="avatar_from_betas", help="Name of created avatar")
@click.option(
    "--model-version",
    type=click.Choice(client.EnumsModelVersion.enum_values(), case_sensitive=False),
    help="Model version",
)
@avatar_download_format
@avatar_download_params
def create_from_betas(
    ctx: click.Context,
    gender: Optional[client.EnumsGender],
    betas: list[float],
    name: str,
    model_version: Optional[client.EnumsModelVersion],
    download_format: str,
    pose: str,
    animation: str,
    compatibility_mode: str,
    out_file: click.Path,
) -> None:
    """Create avatar from betas."""
    timeout = ctx.obj["config"]["cli"]["timeout"]
    avatar = Avatar(api_client=ctx.obj["api_client"])
    avatar.from_betas(
        betas=betas,
        gender=gender,
        name=name,
        model_version=model_version,
        poseName="",
    )
    log.info(f"AssetID: {avatar.asset_id}")

    # Exit here if avatar should not be downloaded
    if download_format:
        avatar.export_avatar(download_format, pose, animation, compatibility_mode, timeout)
        avatar.download(download_format=download_format, out_file=out_file)


@create.command(cls=CustomCommand, name="from-measurements")
@click.pass_context
@click.option(
    "--gender",
    type=click.Choice(client.EnumsGender.enum_values(), case_sensitive=False),
    required=True,
    help="Gender of created avatar",
)
@click.option("--name", type=str, default="avatar_from_measurements", help="Name of created avatar")
@click.option("--height", type=float, help="Height")
@click.option("--weight", type=float, help="Weight")
@click.option("--bust-girth", type=float, help="Bust girth")
@click.option("--ankle-girth", type=float, help="Ankle girth")
@click.option("--thigh-girth", type=float, help="Thigh girth")
@click.option("--waist-girth", type=float, help="Waist girth")
@click.option("--armscye-girth", type=float, help="Armscye girth")
@click.option("--top-hip-girth", type=float, help="Top hip girth")
@click.option("--neck-base-girth", type=float, help="Neck base girth")
@click.option("--shoulder-length", type=float, help="Shoulder length")
@click.option("--lower-arm-length", type=float, help="Lower arm length")
@click.option("--upper-arm-length", type=float, help="Upper arm length")
@click.option("--inside-leg-height", type=float, help="Inside leg height")
@click.option(
    "--model-version",
    type=click.Choice(client.EnumsModelVersion.enum_values(), case_sensitive=False),
    help="Model version",
)
@avatar_download_format
@avatar_download_params
def create_from_measurements(
    ctx: click.Context,
    gender: Optional[client.EnumsGender],
    name: str,
    height,
    weight,
    bust_girth,
    ankle_girth,
    thigh_girth,
    waist_girth,
    armscye_girth,
    top_hip_girth,
    neck_base_girth,
    shoulder_length,
    lower_arm_length,
    upper_arm_length,
    inside_leg_height,
    model_version: Optional[client.EnumsModelVersion],
    download_format: str,
    pose: str,
    animation: str,
    compatibility_mode: str,
    out_file: click.Path,
) -> None:
    """Create avatar from measurements."""
    # Create avatar from measurements
    measurements = get_measurements_dict(
        height,
        weight,
        bust_girth,
        ankle_girth,
        thigh_girth,
        waist_girth,
        armscye_girth,
        top_hip_girth,
        neck_base_girth,
        shoulder_length,
        lower_arm_length,
        upper_arm_length,
        inside_leg_height,
    )
    timeout = ctx.obj["config"]["cli"]["timeout"]
    avatar = Avatar(api_client=ctx.obj["api_client"])
    avatar.from_measurements(
        measurements=measurements, gender=gender, name=name, model_version=model_version, timeout=timeout
    )

    log.info(f"AssetID: {avatar.asset_id}")

    # Exit here if avatar should not be downloaded
    if download_format:
        avatar.export_avatar(download_format, pose, animation, compatibility_mode, timeout)
        avatar.download(download_format=download_format, out_file=out_file)


@create.command(cls=CustomCommand, name="from-images")
@click.pass_context
@click.option(
    "--gender",
    type=click.Choice(client.EnumsGender.enum_values(), case_sensitive=False),
    help="Gender of created avatar",
)
@click.option("--name", type=str, default="avatar_from_images", help="Name of created avatar")
@click.option("--input", required=True, type=click.Path(dir_okay=False, exists=True), help="Path to input image")
@click.option("--height", type=int, help="Height of the person in the image")
@click.option("--weight", type=int, help="Weight of the person in the image")
@click.option(
    "--image-mode",
    type=click.Choice(["AFI", "BEDLAM_CLIFF"], case_sensitive=False),
    default="AFI",
    help="Mode for avatar creation",
)
@avatar_download_format
@avatar_download_params
def create_from_images(
    ctx: click.Context,
    gender: Optional[client.EnumsGender],
    name: str,
    input: str,
    height: int,
    weight: int,
    image_mode: str,
    download_format: str,
    pose: str,
    animation: str,
    compatibility_mode: str,
    out_file: click.Path,
) -> None:
    """Create avatar from images."""
    uploader = Uploader()
    timeout = ctx.obj["config"]["cli"]["timeout"]
    avatar = Avatar(api_client=ctx.obj["api_client"])
    avatar.from_images(
        gender=gender,
        name=name,
        input=input,
        height=height,
        weight=weight,
        image_mode=image_mode,
        uploader=uploader,
        timeout=timeout,
    )

    log.info(f"AssetID: {avatar.asset_id}")

    # Exit here if avatar should not be downloaded
    if download_format:
        avatar.export_avatar(download_format, pose, animation, compatibility_mode, timeout)
        avatar.download(download_format=download_format, out_file=out_file)


@create.command(cls=CustomCommand, name="from-scans")
@click.pass_context
@click.option(
    "--gender",
    type=click.Choice(client.EnumsGender.enum_values(), case_sensitive=False),
    help="Gender of created avatar",
)
@click.option("--name", type=str, default="avatar_from_scans", help="Name of created avatar")
@click.option("--input", type=click.Path(dir_okay=False, exists=True), help="Path to input image")
@click.option("--init-pose", type=str, help="Pose for initialization")
@click.option("--up-axis", type=str, help="Up axis")
@click.option("--look-axis", type=str, help="Look axis")
@click.option("--input-units", type=str, help="Input units of scan")
@avatar_download_format
@avatar_download_params
def create_from_scans(
    ctx: click.Context,
    gender: Optional[client.EnumsGender],
    name: str,
    input: str,
    init_pose: str,
    up_axis: str,
    look_axis: str,
    input_units: str,
    download_format: str,
    pose: str,
    animation: str,
    compatibility_mode: str,
    out_file: click.Path,
) -> None:
    """Create avatar from scans."""
    uploader = Uploader()
    timeout = ctx.obj["config"]["cli"]["timeout"]
    avatar = Avatar(api_client=ctx.obj["api_client"])
    avatar.from_scans(
        gender=gender,
        name=name,
        input=input,
        init_pose=init_pose,
        up_axis=up_axis,
        look_axis=look_axis,
        input_units=input_units,
        uploader=uploader,
        timeout=timeout,
    )

    log.info(f"AssetID: {avatar.asset_id}")

    # Exit here if avatar should not be downloaded
    if download_format:
        avatar.export_avatar(download_format, pose, animation, compatibility_mode, timeout)
        avatar.download(download_format=download_format, out_file=out_file)


@create.command(cls=CustomCommand, name="from-video")
@click.pass_context
@click.option(
    "--multi-person/--single-person",
    default=False,
    callback=validate_person_mode_download_format,
    help="Specify --multi-person to produce a scene with multiple avatars. "
    "Option --single-person is the default and produces a single avatar.",
)
@click.option(
    "--gender",
    type=click.Choice(client.EnumsGender.enum_values(), case_sensitive=False),
    help="Gender of created avatar",
)
@click.option("--name", type=str, default="avatar_from_video", help="Name of created avatar")
@click.option("--input", type=click.Path(dir_okay=False, exists=True), required=True, help="Path to input video")
@avatar_scene_download_format
@avatar_download_params
def create_from_video(
    ctx: click.Context,
    multi_person: bool,
    gender: Optional[client.EnumsGender],
    name: str,
    input: str,
    download_format: str,
    pose: str,
    animation: str,
    compatibility_mode: str,
    out_file: click.Path,
) -> None:
    """Create scene or avatar from a single video. To create a scene with multiple avatars,
    use mcme create from-video --multi-person."""
    uploader = Uploader()
    timeout = ctx.obj["config"]["cli"]["timeout"]
    if not multi_person:
        # Create single avatar
        avatar = Avatar(api_client=ctx.obj["api_client"])
        avatar.from_video(gender=gender, name=name, input=input, uploader=uploader, timeout=timeout)
        log.info(f"AssetID: {avatar.asset_id}")
        # Exit here if avatar should not be downloaded
        if download_format:
            avatar.export_avatar(download_format, pose, animation, compatibility_mode, timeout)
            avatar.download(download_format=download_format, out_file=out_file)
    else:
        # Create scene
        scene = Scene(api_client=ctx.obj["api_client"])
        scene.from_video(gender=gender, name=name, input=input, uploader=uploader, timeout=timeout)
        log.info(f"AssetID: {scene.asset_id}")
        if download_format:
            scene.update_download_url()
            scene.download(download_format=download_format, out_file=out_file)


@create.command(cls=CustomCommand, name="from-text")
@click.pass_context
@click.option("--prompt", type=str, required=True, help="Text prompt describing desired motion")
@click.option("--name", type=str, help="Name of created avatar")
@avatar_download_format
@avatar_download_params
def create_from_text(
    ctx: click.Context,
    prompt: str,
    name: str,
    download_format: str,
    pose: str,
    animation: str,
    compatibility_mode: str,
    out_file: click.Path,
) -> None:
    """Create avatar with motion from text prompt."""
    timeout = ctx.obj["config"]["cli"]["timeout"]

    if name is None:
        name = prompt.replace(" ", "_")

    motion = Motion(api_client=ctx.obj["api_client"])

    # Search for motion by prompt and save temporary smpl file
    motion.find_from_text(prompt=prompt)
    motion.download_temp_smpl()
    # Trim motion to relevant frames
    motion.trim()

    # Use found and trimmed motion .smpl file to create avatar
    uploader = Uploader()
    avatar = Avatar(api_client=ctx.obj["api_client"])
    avatar.from_smpl(motion.trimmed_smpl_file, name=name, uploader=uploader, timeout=timeout)

    log.info(f"AssetID: {avatar.asset_id}")

    # Delete temporary motion .smpl file
    motion.cleanup_temp_smpl()

    # Exit here if avatar should not be downloaded
    if download_format:
        avatar.export_avatar(download_format, pose, animation, compatibility_mode, timeout)
        avatar.download(download_format=download_format, out_file=out_file)


@create.command(cls=CustomCommand, name="blend-motions")
@click.pass_context
@click.option(
    "--source-avatar-id", type=str, help="A clone of this avatar will be used to attach the resulting motion to"
)
@click.option("--motion-id-1", type=str, help="First motion to use for blending")
@click.option("--motion-id-2", type=str, help="Second motion to use for blending")
@click.option(
    "--shape-parameters",
    type=click.UNPROCESSED,
    callback=partial(parse_betas, is_smplx=True),
    help='''If source-avatar-id is not specified, these SMPLX shape parameters will be used to create avatar from. 
    Supply like 0.1,0.2 or "[0.1,0.2]"''',
)
@click.option(
    "--gender",
    type=click.Choice(client.EnumsGender.enum_values(), case_sensitive=False),
    help="If source-avatar-id is not specified, this gender will be used for created avatar.",
)
@click.option("--name", type=str, default="avatar_from_blend_motion", help="Name of created avatar")
@avatar_download_format
@avatar_download_params
def create_blend_motions(
    ctx: click.Context,
    source_avatar_id: str,
    motion_id_1: str,
    motion_id_2: str,
    shape_parameters: Optional[list[float]],
    gender: Optional[client.EnumsGender],
    name: str,
    download_format: str,
    pose: str,
    animation: str,
    compatibility_mode: str,
    out_file: click.Path,
) -> None:
    """Create avatar with blended motion attached."""
    if shape_parameters == []:
        shape_parameters = None
    timeout = ctx.obj["config"]["cli"]["timeout"]
    ready_assets = Motion.get_ready_assets(api_client=ctx.obj["api_client"], show_max_assets=10)
    select_motion = partial(
        Motion.select_asset,
        columns=["Asset ID", "Created from", "Created at"],
        ready_assets=ready_assets,
        api_client=ctx.obj["api_client"],
    )
    first_motion: Motion = (
        select_motion(prompt_message="Select first motion")
        if motion_id_1 is None
        else Motion.create_from_asset_id(api_client=ctx.obj["api_client"], asset_id=motion_id_1)
    )
    second_motion: Motion = (
        select_motion(prompt_message="Select second motion")
        if motion_id_2 is None
        else Motion.create_from_asset_id(api_client=ctx.obj["api_client"], asset_id=motion_id_2)
    )

    avatar = Avatar(api_client=ctx.obj["api_client"])
    avatar.blend_motions(
        source_avatar_id=source_avatar_id,
        motion_id_1=first_motion.asset_id,
        motion_id_2=second_motion.asset_id,
        shape_parameters=shape_parameters,
        gender=gender,
        name=name,
        timeout=timeout,
    )

    log.info(f"AssetID: {avatar.asset_id}")

    # Exit here if avatar should not be downloaded
    if download_format:
        if download_format != "FBX" or pose != "SCAN":
            raise click.BadArgumentUsage(
                """Dowwnload format has to be FBX and pose has to be SCAN 
                to attach blended motion to the resulting avatar."""
            )
        avatar.export_avatar(
            download_format=download_format,
            pose=pose,
            animation=animation,
            compatibility_mode=compatibility_mode,
            timeout=timeout,
        )
        avatar.download(download_format=download_format, out_file=out_file)


# TODO: reimplement batch processing


@cli.command(name="download")
@require_auth
@click.pass_context
@click.option(
    "--format",
    type=click.Choice(["OBJ", "FBX"], case_sensitive=False),
    default="OBJ",
    help="Format for downloading avatar",
)
@click.option(
    "--pose",
    type=click.Choice(["T", "A", "SCAN", "U", "I", "W"], case_sensitive=False),
    default="A",
    help="Pose the downloaded avatar should be in",
)
@click.option(
    "--animation", type=click.Choice(["a-salsa"], case_sensitive=False), help="Animation for the downloaded avatar"
)
@click.option(
    "--compatibility-mode",
    type=click.Choice(["DEFAULT", "OPTITEX", "UNREAL"], case_sensitive=False),
    help="Compatibility mode",
)
@click.option("--out-file", type=click.Path(dir_okay=False), help="File to save created avatar mesh to")
@click.option("--asset-id", type=str, help="Asset id of avatar to be downloaded")
@click.option(
    "--show-max-avatars",
    type=int,
    default=10,
    help="Maximum number of created avatars to show (most recent ones are shown first)",
)
def export_and_download_avatar(
    ctx: click.Context,
    format: str,
    pose: str,
    animation: str,
    compatibility_mode: str,
    out_file: click.Path,
    asset_id: str,
    show_max_avatars: int,
) -> None:
    """
    Export avatar using asset id.
    """
    # show avatar selection dialogue if asset id is not supplied
    if asset_id is None:
        ready_assets = Avatar.get_ready_assets(api_client=ctx.obj["api_client"], show_max_assets=show_max_avatars)
        avatar = Avatar.select_asset(
            api_client=ctx.obj["api_client"],
            ready_assets=ready_assets,
            columns=["Name", "Asset ID", "Created from", "Created at"],
            prompt_message="Number of avatar to download",
        )
    else:
        avatar = Avatar(ctx.obj["api_client"])
        avatar.set_asset_id(asset_id=asset_id)
        avatar.update()

    # Export avatar
    timeout = ctx.obj["config"]["cli"]["timeout"]
    avatar.export_avatar(
        download_format=format, pose=pose, animation=animation, compatibility_mode=compatibility_mode, timeout=timeout
    )
    out_filename = (
        str(out_file)
        if out_file is not None
        else f"{get_timestamp()}_{avatar.name}.{format.lower()}"
        if (avatar.name is not None and avatar.name != "")
        else f"{get_timestamp()}_{asset_id}.{format.lower()}"
    )
    avatar.download(download_format=format, out_file=out_filename)


@cli.command()
@click.pass_context
def info(ctx: click.Context) -> None:
    """Show API info."""
    # Create an instance of the API class
    api_instance = client.InfoApi(ctx.obj["api_client"])

    try:
        # Show API info
        api_response: str = api_instance.info()
        log.info(api_response)
    except Exception as e:
        log.info("Exception when calling InfoApi->info: %s\n" % e)


@cli.command(name="user-info")
@require_auth
@click.pass_context
def user_info(ctx: click.Context) -> None:
    """Show username and available credits."""
    api_instance_user = client.UserApi(ctx.obj["api_client"])

    user = request_user_info(api_instance_user)

    log.info(f"Username: {user.email}")
    log.info(f"Credits: {user.credits}")
