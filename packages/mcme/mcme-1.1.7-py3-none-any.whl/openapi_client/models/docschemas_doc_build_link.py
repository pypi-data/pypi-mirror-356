# coding: utf-8

"""
    Meshcapade Me API

    Welcome to the age of Avatars, introducing the Meshcapade Me API. The no-friction avatar-creation platform for all your avatar needs. Create accurate digital doubles from any source of data in a unified 3D body format for every industry. Built on our <a href=\"https://meshcapade.com/SMPL\" target=\"_blank\">patented avatar</a> technology, our API allows you to create and edit avatars from images, videos, measurements, scans, and more. # Introduction The Meshcapade Me API is a RESTful API that allows you to create and edit avatars from images, measurements, scans, and more. All API replies adhere to the  <a href=\"https://jsonapi.org/format/\" target=\"_blank\">JSON:API</a> schema guidelines. Currently the API is in beta and is subject to change. Thus, not all ways to create avatars are available yet. We are working hard to add more ways to create avatars and will update this documentation accordingly. The API allows you to create avatars </br> - From <a href=\"#post-/avatars/create/from-images\" target=\"_blank\">images</a> </br> - From <a href=\"#post-/avatars/create/from-video\" target=\"_blank\">video</a> </br> - From <a href=\"#post-/avatars/create/from-scans\" target=\"_blank\">3D scans</a> </br> - From <a href=\"#post-/avatars/create/from-measurements\" target=\"_blank\">measurements</a> </br> # Quickstart To get started, sign up for a free account at <a href=\"https://me.meshcapade.com\" target=\"_blank\">me.meshcapade.com</a></br> We recommend using our <a href=\"https://www.postman.com/downloads/\" target=\"_blank\">Postman</a> collection to conveniently explore the API </br> <div style=\"margin-top: 16px;\"><a href=\"https://www.postman.com/cloudy-meadow-883625/workspace/meshcapade/overview\"><img src=\"https://run.pstmn.io/button.svg\" alt=\"Run in Postman\"></a></div></br>  # How-To <a href=\"https://medium.com/meshcapade/streamline-avatar-creation-with-meshcapade-me-api-from-one-image-to-an-accurate-avatar-in-seconds-b8ca4f15b9a8\" target=\"_blank\">Create an avatar from a single image (Medium)</a> </br> <a href=\"https://medium.com/meshcapade/measurements-meet-imagination-creating-accurate-3d-avatars-with-meshcapades-api-9a6ec5029793\" target=\"_blank\">Create an avatar from measurements (Medium)</a> # API Categories The API is organized into the following main categories: - Assets </br> Endpoint for listing assets of multiple types. - Avatars </br> Endpoints for listing, downloading, and deleting avatars. - Mesh </br> Endpoints for listing, downloading, and deleting exported meshes. - Images </br> Endpoints for listing, uploading, and deleting images related to avatars. - Create Avatar from images </br> Endpoints to initiate and complete avatar creation from images. - Create Avatar from measurements </br> Endpoint to initiate avatar creation from body measurements. - Create Avatar from scans </br> Endpoints to initiate and complete avatar creation from 3d body scans. - Create Avatar from betas </br> Endpoint to create an avatar from SMPL based beta shape parameters. # Error codes When something goes wrong, the API replies with an additional error code  - `asset_not_found` The requested asset either does not exist, or is not owned by the user (404)  </br> - `too_many_images` The image limit that can be uploaded for avatars from images as been exceeded. (400) </br> - `already_started` A process that already has been requested cannot be started again. (400) </br> - `no_images`  [POST /avatars/create/from-images](#post-/avatars/create/from-images) can only be started with at least one image uploaded  (400) </br> - `inputs_not_ready` Running `/avatars/create/xxxx` endpoint require the inputs to be uploaded (400) </br> - `uuid_invalid_format` Asset ID is in a non-UUID format (400) </br> - ` missing_parameters` Not all required parameters have been supplied for the request (400) </br> - `unauthorized` Trying to access an asset the user does not own, or endpoints that the user is not authorized to call (400) </br> - `too_many_builds` User processing rate has been exceeded. Only one computation heavy process can be started at a time (429) </br> - `asset_not_ready` Cannot call request on an asset which is not in a READY state (400) </br>  # Integration When integrating with our API, you may encounter Cross-Origin Resource Sharing (CORS) issues during deployment. </br> For security reasons, our API does not support direct communication from your frontend. </br> Instead, we recommend that you connect to api.meshcapade through your own backend server. </br> This approach not only mitigates CORS-related challenges but also enhances the overall security of your application. </br> By handling API requests server-side, you can ensure smoother and safer integration. </br> If you encounter any issues during integration, please reach out to us at support@meshcapade.com </br>  # noqa: E501

    The version of the OpenAPI document: v1.20
    Contact: support@meshcapade.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Optional
from pydantic import BaseModel, Field, StrictStr

class DocschemasDocBuildLink(BaseModel):
    """
    DocschemasDocBuildLink
    """
    var_self: Optional[StrictStr] = Field(None, alias="self")
    __properties = ["self"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> DocschemasDocBuildLink:
        """Create an instance of DocschemasDocBuildLink from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> DocschemasDocBuildLink:
        """Create an instance of DocschemasDocBuildLink from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return DocschemasDocBuildLink.parse_obj(obj)

        _obj = DocschemasDocBuildLink.parse_obj({
            "var_self": obj.get("self")
        })
        return _obj

