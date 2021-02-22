import itertools
from typing import Union, List

import callofduty
import callofduty.http
import callofduty.utils
from callofduty import Title, Platform, Mode, Match
from avoid_loop_import import get_channel_by_name, ERROR_CHANNEL

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
    async def SearchPlayers(self, platform: Platform, username: str, **kwargs):
        return await super().SearchPlayers(platform, username, **kwargs)


async def DorLogin(email: str, password: str) -> DorClient:
    auth: callofduty.auth.Auth = callofduty.auth.Auth(email, password)
    await auth.RegisterDevice()
    await auth.SubmitLogin()
    return DorClient(DorHTTP(auth))

class credentials:
    def __init__(self, credential_list: list):
        self.credential_list = credential_list
        self.use = credential_list[0].split(':')
        self.index = 0

    def next_use(self):
        self.index = self.index + 1 % len(self.credential_list)
        self.use = self.credential_list[self.index].split(':')
        return self.use


gen = credentials(CREDENTIAL_LIST)


# def _get_connection_credentials():
#     for credentials in itertools.cycle(CREDENTIAL_LIST):
#         yield credentials.split(':')


class WithRetry:

    def __init__(self, func, number_of_retries=None):
        if number_of_retries is None:
            number_of_retries = len(CREDENTIAL_LIST)

        self._number_of_retries = number_of_retries
        self._func = func

    async def __call__(self, *args, **kwargs):
        for _ in range(self._number_of_retries):
            email, password = gen.use
            gen.next_use()
            try:
                client = await DorLogin(email, password)
                return_value = await self._func(client, *args, **kwargs)
                await ErorrChannel.send(
                    f'**This email_client is work {email}**, for method **{self._func.__name__}**'
                )
            except Exception:
                ErorrChannel = get_channel_by_name(ERROR_CHANNEL)
                await ErorrChannel.send(
                    f'I tried to use user **{email}**, for method **{self._func.__name__}** and the request failed!'
                )
                continue
            return return_value

        raise Exception()


class CodClient:

    def __init__(self, number_of_retries=None):
        if number_of_retries is None:
            number_of_retries = len(CREDENTIAL_LIST)

        self._number_of_retries = number_of_retries

    @property
    def number_of_retries(self):
        return self._number_of_retries

    def __getattr__(self, item):
        return WithRetry(getattr(DorClient, item), number_of_retries=self.number_of_retries)



