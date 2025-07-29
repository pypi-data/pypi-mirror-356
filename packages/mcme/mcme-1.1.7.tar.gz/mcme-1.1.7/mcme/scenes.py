from typing import Optional
import openapi_client as client
from .helpers import Uploader
from .assets import Asset, CreateFromSourceMixin


class Scene(CreateFromSourceMixin, Asset):
    """Represents a scene asset.

    This class inherits from Asset as well as from mixin classes to add functionality not unique to scenes.
    """

    asset_api = client.ScenesApi
    list_method_name = "describe_scene"
    list_all_method_name = ""
    # TODO add list_all_method_name, requires action in meshcapade-me-api

    def from_video(
        self,
        gender: Optional[client.EnumsGender],
        name: str,
        input: str,
        uploader: Uploader,
        timeout: int,
    ):
        """Creates a scene from a video."""
        from_video_api = client.CreateSceneFromVideoApi(self.api_client)
        initialize_asset_method = from_video_api.create_scene_from_video
        request_upload_method = from_video_api.upload_video_to_scene
        fit_to_source_method = from_video_api.scene_fit_to_video
        request_parameters = client.DocschemasDocAFVInputs(avatarname=name, gender=gender, modelVersion=None)
        self.set_name(name)
        self.create_from_source(
            initialize_asset_method=initialize_asset_method,
            request_upload_method=request_upload_method,
            fit_to_source_method=fit_to_source_method,
            input=input,
            request_parameters=request_parameters,
            uploader=uploader,
            timeout=timeout,
        )
