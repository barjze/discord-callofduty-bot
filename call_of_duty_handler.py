import itertools
from typing import Union, List

import callofduty
import callofduty.http
import callofduty.utils
from callofduty import Title, Platform, Mode, Match


CREDENTIAL_LIST = [
    'almog889@gmail.com:An130991',
    'sihmon.tally@gmail.com:Alon2253',
    'moranmoradi20@gmail.com:moran689',
    'bigfancod@gmail.com:callofduty2@',
    'ovo6owl@hotmail.com:Artemis1!2@',
    'linanachshon1@gmail.com:Ln261155',
    'kayosha2020@gmail.com:Kaya2020'
]


class DorHTTP(callofduty.http.HTTP):
    def __init__(self, auth):
        super().__init__(auth)

    async def GetFullMatch(self, title: str, platform: str, mode: str, match_id: int, **kwargs) -> Union[dict, list, str]:
        return await self.Send(
            callofduty.http.Request(
                "GET",
                f"api/papi-client/crm/cod/v2/title/{title}/platform/{platform}/fullMatch/{mode}/{matchId}/en",
            )
        )


class DorMatch(callofduty.match.Match):

    def __init__(self, client: 'DorClient', **kwargs):
        super().__init__(client, kwargs)

    async def details(self) -> dict:
        return await self._client.GetFullMatch(self.title, self.platform, self.id, )


class DorClient(callofduty.Client):
    def __init__(self, http):
        super().__init__(http)

    async def GetFullMatch(self, title: Title, platform: Platform, match_id: int, **kwargs) -> dict:
        callofduty.utils.VerifyTitle(title)
        callofduty.utils.VerifyPlatform(platform)

        return (
            await self.http.GetFullMatch(title.value, platform.value, Mode.Warzone.value, )
        )["data"]

    async def GetPlayerMatches(
            self, platform: Platform, username: str, title: Title, mode: Mode, **kwargs
    ) -> List[Match]:
        matches = await super().GetPlayerMatches(platform, username, title, mode, **kwargs)

        return [
            DorMatch(self, id=match.id, platform=match.platform, title=match.title)
            for match
            in matches
        ]


async def DorLogin(email: str, password: str) -> DorClient:
    auth: callofduty.auth.Auth = callofduty.auth.Auth(email, password)
    await auth.RegisterDevice()
    await auth.SubmitLogin()
    return DorClient(DorHTTP(auth))


def _get_connection_credentials():
    for credentials in CREDENTIAL_LIST:
        yield credentials.split(':')


def get_cod_client():
    return await DorLogin(*_get_connection_credentials())
