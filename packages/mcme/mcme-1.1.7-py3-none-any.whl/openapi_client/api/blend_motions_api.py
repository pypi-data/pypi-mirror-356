# coding: utf-8

"""
    Meshcapade Me API

    Welcome to the age of Avatars, introducing the Meshcapade Me API. The no-friction avatar-creation platform for all your avatar needs. Create accurate digital doubles from any source of data in a unified 3D body format for every industry. Built on our <a href=\"https://meshcapade.com/SMPL\" target=\"_blank\">patented avatar</a> technology, our API allows you to create and edit avatars from images, videos, measurements, scans, and more. # Introduction The Meshcapade Me API is a RESTful API that allows you to create and edit avatars from images, measurements, scans, and more. All API replies adhere to the  <a href=\"https://jsonapi.org/format/\" target=\"_blank\">JSON:API</a> schema guidelines. Currently the API is in beta and is subject to change. Thus, not all ways to create avatars are available yet. We are working hard to add more ways to create avatars and will update this documentation accordingly. The API allows you to create avatars </br> - From <a href=\"#post-/avatars/create/from-images\" target=\"_blank\">images</a> </br> - From <a href=\"#post-/avatars/create/from-video\" target=\"_blank\">video</a> </br> - From <a href=\"#post-/avatars/create/from-scans\" target=\"_blank\">3D scans</a> </br> - From <a href=\"#post-/avatars/create/from-measurements\" target=\"_blank\">measurements</a> </br> # Quickstart To get started, sign up for a free account at <a href=\"https://me.meshcapade.com\" target=\"_blank\">me.meshcapade.com</a></br> We recommend using our <a href=\"https://www.postman.com/downloads/\" target=\"_blank\">Postman</a> collection to conveniently explore the API </br> <div style=\"margin-top: 16px;\"><a href=\"https://www.postman.com/cloudy-meadow-883625/workspace/meshcapade/overview\"><img src=\"https://run.pstmn.io/button.svg\" alt=\"Run in Postman\"></a></div></br>  # How-To <a href=\"https://medium.com/meshcapade/streamline-avatar-creation-with-meshcapade-me-api-from-one-image-to-an-accurate-avatar-in-seconds-b8ca4f15b9a8\" target=\"_blank\">Create an avatar from a single image (Medium)</a> </br> <a href=\"https://medium.com/meshcapade/measurements-meet-imagination-creating-accurate-3d-avatars-with-meshcapades-api-9a6ec5029793\" target=\"_blank\">Create an avatar from measurements (Medium)</a> # API Categories The API is organized into the following main categories: - Assets </br> Endpoint for listing assets of multiple types. - Avatars </br> Endpoints for listing, downloading, and deleting avatars. - Mesh </br> Endpoints for listing, downloading, and deleting exported meshes. - Images </br> Endpoints for listing, uploading, and deleting images related to avatars. - Create Avatar from images </br> Endpoints to initiate and complete avatar creation from images. - Create Avatar from measurements </br> Endpoint to initiate avatar creation from body measurements. - Create Avatar from scans </br> Endpoints to initiate and complete avatar creation from 3d body scans. - Create Avatar from betas </br> Endpoint to create an avatar from SMPL based beta shape parameters. # Error codes When something goes wrong, the API replies with an additional error code  - `asset_not_found` The requested asset either does not exist, or is not owned by the user (404)  </br> - `too_many_images` The image limit that can be uploaded for avatars from images as been exceeded. (400) </br> - `already_started` A process that already has been requested cannot be started again. (400) </br> - `no_images`  [POST /avatars/create/from-images](#post-/avatars/create/from-images) can only be started with at least one image uploaded  (400) </br> - `inputs_not_ready` Running `/avatars/create/xxxx` endpoint require the inputs to be uploaded (400) </br> - `uuid_invalid_format` Asset ID is in a non-UUID format (400) </br> - ` missing_parameters` Not all required parameters have been supplied for the request (400) </br> - `unauthorized` Trying to access an asset the user does not own, or endpoints that the user is not authorized to call (400) </br> - `too_many_builds` User processing rate has been exceeded. Only one computation heavy process can be started at a time (429) </br> - `asset_not_ready` Cannot call request on an asset which is not in a READY state (400) </br>  # Integration When integrating with our API, you may encounter Cross-Origin Resource Sharing (CORS) issues during deployment. </br> For security reasons, our API does not support direct communication from your frontend. </br> Instead, we recommend that you connect to api.meshcapade through your own backend server. </br> This approach not only mitigates CORS-related challenges but also enhances the overall security of your application. </br> By handling API requests server-side, you can ensure smoother and safer integration. </br> If you encounter any issues during integration, please reach out to us at support@meshcapade.com </br>  # noqa: E501

    The version of the OpenAPI document: v1.20
    Contact: support@meshcapade.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


import re  # noqa: F401
import io
import warnings

from pydantic import validate_arguments, ValidationError
from typing_extensions import Annotated

from typing_extensions import Annotated
from pydantic import Field

from openapi_client.models.docschemas_doc_base_single_jsonapi_response import DocschemasDocBaseSingleJSONAPIResponse
from openapi_client.models.schemas_motion_blend_request import SchemasMotionBlendRequest

from openapi_client.api_client import ApiClient
from openapi_client.api_response import ApiResponse
from openapi_client.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class BlendMotionsApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client

    @validate_arguments
    def blend_motions(self, blend_motions_request : Annotated[SchemasMotionBlendRequest, Field(..., description="The motions to blend")], **kwargs) -> DocschemasDocBaseSingleJSONAPIResponse:  # noqa: E501
        """Blend two motions together  # noqa: E501

        Blends two motions into a single consistent motion. If `sourceAvatarID` is supplied, a clone of the avatar will be used to attach the resulting motion to. If `sourceAvatarID` is not supplied, a new avatar will be created using the SMPLX based `shapeParameters` and `gender` (`female`, `male`, `neutral`) fields.\\ The input motion IDs must be different IDs. Both motions have to be in `READY` state.\\ Additionally, the motions have to have at least 15 frames. Single pose motions as produced by creating avatars from images are not accepted yet. \\ FPS of the input motions have to be between 15 and 60 frames per second. Any FPS value in this range is resampled to 30 FPS. \\ <b>This is a paid endpoint for accounts on a PRO subscription</b> and requires credits to be available on the user's account. Blending two motions costs 100 credits. Check out the <a href=\"https://me.meshcapade.com/credits\">credits</a> page for more information on credits. \\ Head over to the <a href=\"https://me.meshcapade.com/subscriptions\">subscriptions</a> page to upgrade your account to PRO.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.blend_motions(blend_motions_request, async_req=True)
        >>> result = thread.get()

        :param blend_motions_request: The motions to blend (required)
        :type blend_motions_request: SchemasMotionBlendRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: DocschemasDocBaseSingleJSONAPIResponse
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the blend_motions_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.blend_motions_with_http_info(blend_motions_request, **kwargs)  # noqa: E501

    @validate_arguments
    def blend_motions_with_http_info(self, blend_motions_request : Annotated[SchemasMotionBlendRequest, Field(..., description="The motions to blend")], **kwargs) -> ApiResponse:  # noqa: E501
        """Blend two motions together  # noqa: E501

        Blends two motions into a single consistent motion. If `sourceAvatarID` is supplied, a clone of the avatar will be used to attach the resulting motion to. If `sourceAvatarID` is not supplied, a new avatar will be created using the SMPLX based `shapeParameters` and `gender` (`female`, `male`, `neutral`) fields.\\ The input motion IDs must be different IDs. Both motions have to be in `READY` state.\\ Additionally, the motions have to have at least 15 frames. Single pose motions as produced by creating avatars from images are not accepted yet. \\ FPS of the input motions have to be between 15 and 60 frames per second. Any FPS value in this range is resampled to 30 FPS. \\ <b>This is a paid endpoint for accounts on a PRO subscription</b> and requires credits to be available on the user's account. Blending two motions costs 100 credits. Check out the <a href=\"https://me.meshcapade.com/credits\">credits</a> page for more information on credits. \\ Head over to the <a href=\"https://me.meshcapade.com/subscriptions\">subscriptions</a> page to upgrade your account to PRO.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.blend_motions_with_http_info(blend_motions_request, async_req=True)
        >>> result = thread.get()

        :param blend_motions_request: The motions to blend (required)
        :type blend_motions_request: SchemasMotionBlendRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(DocschemasDocBaseSingleJSONAPIResponse, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'blend_motions_request'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method blend_motions" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['blend_motions_request'] is not None:
            _body_params = _params['blend_motions_request']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/json']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['OAuth2Password', 'Bearer']  # noqa: E501

        _response_types_map = {
            '200': "DocschemasDocBaseSingleJSONAPIResponse",
        }

        return self.api_client.call_api(
            '/motions/blend', 'POST',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))
