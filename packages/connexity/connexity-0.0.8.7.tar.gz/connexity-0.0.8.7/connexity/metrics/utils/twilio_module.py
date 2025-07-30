from asyncio import sleep
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client


class TwilioCallManager:
    def __init__(self, account_sid, auth_token):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.client = Client(self.account_sid, self.auth_token)

    async def get_call_duration(self, call_sid):

        call = self.client.calls(call_sid).fetch()

        duration = call.duration
        return duration

    async def get_call_recording_url(
            self,
            call_sid: str,
            *,
            max_retries: int = 3,
            delay_sec: int = 3
    ) -> str | None:
        """
        Try fetching the specific recording you just created.
        Retry up to max_retries times on 404.
        """
        for attempt in range(1, max_retries + 1):
            try:
                recordings = self.client.recordings.list(call_sid=call_sid)
                if recordings:
                # success!
                    sid = recordings[0].sid
                    recording_url = f"https://api.twilio.com/2010-04-01/Accounts/{self.account_sid}/Recordings/{sid}.wav"
                    return recording_url
            except TwilioRestException as e:
                # only retry on “not yet available” errors
                if e.status == 404 and attempt < max_retries:
                    print(f"⚠️ attempt {attempt} got 404, sleeping {delay_sec}s…")
                    await sleep(delay_sec)
                    continue
        print("❌ Giving up after retries, recording still not found.")
        return None

    async def get_start_call_data(self, call_sid):

        call = self.client.calls(call_sid).fetch()

        start_time = call.start_time.isoformat().replace("+00:00", "Z")
        return start_time

    def start_call_recording(self, call_sid):
        recording = self.client.calls(call_sid).recordings.create()
        print(f"Recording started with SID: {recording.sid}")