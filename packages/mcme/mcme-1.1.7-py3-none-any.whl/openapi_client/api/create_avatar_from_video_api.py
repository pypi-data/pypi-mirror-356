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
from pydantic import Field, StrictStr

from openapi_client.models.docschemas_doc_afv_inputs import DocschemasDocAFVInputs
from openapi_client.models.docschemas_doc_base_single_jsonapi_response import DocschemasDocBaseSingleJSONAPIResponse

from openapi_client.api_client import ApiClient
from openapi_client.api_response import ApiResponse
from openapi_client.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class CreateAvatarFromVideoApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client

    @validate_arguments
    def avatar_fit_to_video(self, asset_id : Annotated[StrictStr, Field(..., description="Avatar ID")], input : Annotated[DocschemasDocAFVInputs, Field(..., description="Request parameters")], **kwargs) -> DocschemasDocBaseSingleJSONAPIResponse:  # noqa: E501
        """Start fitting process to Video  # noqa: E501

        Starts the fitting process to create an avatar from Video. </br> Call endpoint [POST /avatars/create/from-video](#post-/avatars/create/from-video) before calling this endpoint. </br> Has to be run on the same avatar as the preparation call. One video has to be uploaded before starting the fitting process. </br> The fitting process might take a couple of minutes to complete. This will be indicated by the status of the avatar. </br> <b>This is a paid endpoint</b> and requires credits to be available on the user's account. Creating an avatar from images costs 500 credits. </br> Check out the <a href=\"https://me.meshcapade.com/credits\">credits</a> page for more information on credits. </br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.avatar_fit_to_video(asset_id, input, async_req=True)
        >>> result = thread.get()

        :param asset_id: Avatar ID (required)
        :type asset_id: str
        :param input: Request parameters (required)
        :type input: DocschemasDocAFVInputs
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
            raise ValueError("Error! Please call the avatar_fit_to_video_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.avatar_fit_to_video_with_http_info(asset_id, input, **kwargs)  # noqa: E501

    @validate_arguments
    def avatar_fit_to_video_with_http_info(self, asset_id : Annotated[StrictStr, Field(..., description="Avatar ID")], input : Annotated[DocschemasDocAFVInputs, Field(..., description="Request parameters")], **kwargs) -> ApiResponse:  # noqa: E501
        """Start fitting process to Video  # noqa: E501

        Starts the fitting process to create an avatar from Video. </br> Call endpoint [POST /avatars/create/from-video](#post-/avatars/create/from-video) before calling this endpoint. </br> Has to be run on the same avatar as the preparation call. One video has to be uploaded before starting the fitting process. </br> The fitting process might take a couple of minutes to complete. This will be indicated by the status of the avatar. </br> <b>This is a paid endpoint</b> and requires credits to be available on the user's account. Creating an avatar from images costs 500 credits. </br> Check out the <a href=\"https://me.meshcapade.com/credits\">credits</a> page for more information on credits. </br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.avatar_fit_to_video_with_http_info(asset_id, input, async_req=True)
        >>> result = thread.get()

        :param asset_id: Avatar ID (required)
        :type asset_id: str
        :param input: Request parameters (required)
        :type input: DocschemasDocAFVInputs
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
            'asset_id',
            'input'
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
                    " to method avatar_fit_to_video" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['asset_id']:
            _path_params['assetID'] = _params['asset_id']


        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['input'] is not None:
            _body_params = _params['input']

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
            '400': "DocschemasDocErrorResponse",
            '401': "DocschemasDocErrorResponse",
            '404': "DocschemasDocErrorResponse",
        }

        return self.api_client.call_api(
            '/avatars/{assetID}/fit-to-video', 'POST',
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

    @validate_arguments
    def create_avatar_from_video(self, **kwargs) -> DocschemasDocBaseSingleJSONAPIResponse:  # noqa: E501
        """Initiate avatar from Video creation  # noqa: E501

        Constructs an empty avatar in preparation for creating an avatar from video. The client has to upload a video to the avatar before starting the fitting process. The uploaded video gets \"attached\" to this avatar. The fitting process might take a couple of minutes to complete. This will be indicated by the status of the avatar. </br> First step is calling this endpoint to create the empty avatar </br> Then request a presigned PUT url to upload your video to from [POST /avatars/{assetID}/video](#post-/avatars/-assetID-/video) </br> After you've uploaded a video you can kick off the inference process to produce the final avatar. </br> Start the process by calling [POST /avatars/{assetID}/fit-to-video](#post-/avatars/-assetID-/fit-to-video)  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.create_avatar_from_video(async_req=True)
        >>> result = thread.get()

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
            raise ValueError("Error! Please call the create_avatar_from_video_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.create_avatar_from_video_with_http_info(**kwargs)  # noqa: E501

    @validate_arguments
    def create_avatar_from_video_with_http_info(self, **kwargs) -> ApiResponse:  # noqa: E501
        """Initiate avatar from Video creation  # noqa: E501

        Constructs an empty avatar in preparation for creating an avatar from video. The client has to upload a video to the avatar before starting the fitting process. The uploaded video gets \"attached\" to this avatar. The fitting process might take a couple of minutes to complete. This will be indicated by the status of the avatar. </br> First step is calling this endpoint to create the empty avatar </br> Then request a presigned PUT url to upload your video to from [POST /avatars/{assetID}/video](#post-/avatars/-assetID-/video) </br> After you've uploaded a video you can kick off the inference process to produce the final avatar. </br> Start the process by calling [POST /avatars/{assetID}/fit-to-video](#post-/avatars/-assetID-/fit-to-video)  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.create_avatar_from_video_with_http_info(async_req=True)
        >>> result = thread.get()

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
                    " to method create_avatar_from_video" % _key
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
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # authentication setting
        _auth_settings = ['OAuth2Password', 'Bearer']  # noqa: E501

        _response_types_map = {
            '200': "DocschemasDocBaseSingleJSONAPIResponse",
            '400': "DocschemasDocErrorResponse",
            '401': "DocschemasDocErrorResponse",
            '404': "DocschemasDocErrorResponse",
        }

        return self.api_client.call_api(
            '/avatars/create/from-video', 'POST',
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

    @validate_arguments
    def upload_video_to_avatar(self, asset_id : Annotated[StrictStr, Field(..., description="Avatar ID")], **kwargs) -> DocschemasDocBaseSingleJSONAPIResponse:  # noqa: E501
        """Request Video upload URL for avatar creation  # noqa: E501

        Request Video upload URL for an avatar.  Creates a link between the video image asset and the avatar asset in preparation for fitting the avatar to the scan. If this endpoint is called, a Video has to be uploaded before starting the fitting process, otherwise it will fail. You can call `DELETE /images/{videoid}` to delete the Video The upload URL is a presigned PUT URL that can be used to upload the file to the server..  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.upload_video_to_avatar(asset_id, async_req=True)
        >>> result = thread.get()

        :param asset_id: Avatar ID (required)
        :type asset_id: str
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
            raise ValueError("Error! Please call the upload_video_to_avatar_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.upload_video_to_avatar_with_http_info(asset_id, **kwargs)  # noqa: E501

    @validate_arguments
    def upload_video_to_avatar_with_http_info(self, asset_id : Annotated[StrictStr, Field(..., description="Avatar ID")], **kwargs) -> ApiResponse:  # noqa: E501
        """Request Video upload URL for avatar creation  # noqa: E501

        Request Video upload URL for an avatar.  Creates a link between the video image asset and the avatar asset in preparation for fitting the avatar to the scan. If this endpoint is called, a Video has to be uploaded before starting the fitting process, otherwise it will fail. You can call `DELETE /images/{videoid}` to delete the Video The upload URL is a presigned PUT URL that can be used to upload the file to the server..  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.upload_video_to_avatar_with_http_info(asset_id, async_req=True)
        >>> result = thread.get()

        :param asset_id: Avatar ID (required)
        :type asset_id: str
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
            'asset_id'
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
                    " to method upload_video_to_avatar" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['asset_id']:
            _path_params['assetID'] = _params['asset_id']


        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # authentication setting
        _auth_settings = ['OAuth2Password', 'Bearer']  # noqa: E501

        _response_types_map = {
            '200': "DocschemasDocBaseSingleJSONAPIResponse",
            '400': "DocschemasDocErrorResponse",
            '401': "DocschemasDocErrorResponse",
            '404': "DocschemasDocErrorResponse",
        }

        return self.api_client.call_api(
            '/avatars/{assetID}/video', 'POST',
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
