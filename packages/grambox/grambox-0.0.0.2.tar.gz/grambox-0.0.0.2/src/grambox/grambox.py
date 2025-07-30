import os
import uuid, secrets, time, json, os, re, random, datetime, mimetypes, html
try:
    import requests, user_agent
    from OneClick import Hunter
except:
    os.system("pip install requests user-agent OneClick")

def cookie(username, password, path='sessions.json'):
    if os.path.exists(path):
        with open(path, 'r') as f:
            sessions = json.load(f)
    else:
        sessions = {}
    if username in sessions:
        return sessions[username]
    agg = Hunter.Services()
    agnt = str(agg).replace('136.0.0.34.124', '237.0.0.14.102').replace(
        '208061712', '373310554')
    url = 'https://i.instagram.com/api/v1/accounts/login/'
    headers = {'X-FB-Client-IP': 'True', 'X-IG-Connection-Type': 'WiFi',
        'Accept-Language': 'en-EN;q=1.0', 'x-fb-rmd': 'state=URL_ELIGIBLE',
        'Host': 'i.instagram.com', 'X-IG-Capabilities': '36r/F/8=',
        'X-Bloks-Version-Id': str(secrets.token_hex(8) * 4),
        'X-IG-App-Locale': 'en', 'X-IG-ABR-Connection-Speed-KBPS': '130',
        'X-IG-Timezone-Offset': '10800', 'X-IG-Mapped-Locale': 'en_EN',
        'Connection': 'keep-alive', 'X-IG-App-ID': '124024574287414',
        'X-FB-Friendly-Name': 'api', 'X-IG-Bandwidth-Speed-KBPS': '303.000',
        'X-Bloks-Is-Panorama-Enabled': 'true', 'Priority': 'u=2, i',
        'X-Pigeon-Rawclienttime': str(time.time()), 'User-Agent': str(agg),
        'X-IG-Family-Device-ID': str(uuid.uuid4()), 'X-MID': str(secrets.
        token_hex(8) * 2), 'X-Tigon-Is-Retry': 'False', 'Content-Length':
        '860', 'X-FB-Connection-Type': 'wifi', 'X-IG-Device-ID': str(uuid.
        uuid4()), 'Content-Type':
        'application/x-www-form-urlencoded; charset=UTF-8',
        'X-FB-Server-Cluster': 'True', 'X-IG-Connection-Speed': '0kbps',
        'IG-INTENDED-USER-ID': '0', 'X-IG-Device-Locale': 'en-JO',
        'X-FB-HTTP-Engine': 'Liger'}
    data = {'phone_id': str(uuid.uuid4()), 'reg_login': '0', 'device_id':
        str(uuid.uuid4()), 'has_seen_aart_on': '0', 'username': str(
        username), 'adid': str(uuid.uuid4()), 'login_attempt_count': '0',
        'enc_password': f'#PWD_INSTAGRAM:0:{str(int(time.time()))}:{password}'}
    req = requests.post(url, headers=headers, data=data)
    if 'logged_in_user' in req.text:
        coc = req.headers.get('Set-Cookie')
        token = req.headers.get('ig-set-authorization')
        claim = req.headers.get('x-ig-set-www-claim')
        session_data = {'username': username, 'sessionid': re.search(
            'sessionid=([^;]+)', coc).group(1), 'ds_user_id': re.search(
            'ds_user_id=([^;]+)', coc).group(1), 'csrftoken': re.search(
            'csrftoken=([^;]+)', coc).group(1), 'mid': re.search(
            'mid=([^;]+)', coc).group(1), 'token': token, 'claim': claim,
            'User-Agent': agnt}
        sessions[username] = session_data
        with open(path, 'w') as f:
            json.dump(sessions, f, indent=4)
        return session_data
    else:
        return False, req.text


def delete_session(username, path='sessions.json'):
    if not os.path.exists(path):
        return False, 'no_file_sessions'
    with open(path, 'r') as f:
        sessions = json.load(f)
    if username in sessions:
        del sessions[username]
        with open(path, 'w') as f:
            json.dump(sessions, f, indent=4)
        return True, 'The session has been deleted.'
    return False, 'The session does not exist'


def userid(username, password, user_target):
    ck = cookie(username, password)
    if ck == False:
        return False, ck
    url = (
        f'https://i.instagram.com/api/v1/users/web_profile_info/?username={user_target}'
        )
    h = {'User-Agent': ck['User-Agent'], 'Authorization': ck['token'],
        'Accept-Language': 'ar-EG, en-US'}
    r = requests.get(url, headers=h)
    if r.status_code == 200 and 'biography' in r.text:
        jd = r.json()['data']['user']
        return str(jd.get('id', ''))
    return r.text


def media_id(url):
    try:
        txt = requests.get(url).text
        mid = txt.split('"media_id":"')[1].split('"')[0]
        uid = txt.split('"instapp:owner_user_id" content="')[1].split('"')[0]
        return f'{mid}_{uid}'
    except:
        return None


class GramBox:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.ck = cookie(username, password)
        if self.ck is False:
            raise Exception('Login failed')

    def text_message(self, user_target, txt):
        ck = self.ck
        if ck == False:
            return False, ck
        id = userid(self.username, self.password, user_target)
        url = (
            'https://i.instagram.com/api/v1/direct_v2/threads/broadcast/text/')
        payload = {'action': 'send_item', 'is_x_transport_forward': 'false',
            'is_shh_mode': '0', 'send_silently': 'false',
            'send_attribution': 'direct_inbox', 'client_context': str(uuid.
            uuid4()), 'text': str(txt), 'device_id':
            'android-2f8fe3f996286449', 'mutation_token': str(uuid.uuid4()),
            '_uuid': str(uuid.uuid4()), 'btt_dual_send': 'false',
            'is_ae_dual_send': 'false', 'offline_threading_id': str(uuid.
            uuid4()), 'recipient_users': f'[[{id}]]'}
        headers = {'User-Agent': str(ck['User-Agent']), 'authorization':
            str(ck['token']), 'x-ig-device-id': str(uuid.uuid4())}
        response = requests.post(url, data=payload, headers=headers)
        return response.json()

    def voice_message(self, user_target: str, file_path: str) ->bool:
        try:
            ck = self.ck
            if ck == False:
                return False, ck
            mid = ck['mid']
            token = ck['token']
        except Exception:
            return False
        try:
            user_id = userid(self.username, self.password, user_target)
        except Exception:
            return False
        if not os.path.isfile(file_path):
            return False
        size = os.path.getsize(file_path)
        iid = (
            f'{random.randint(10 ** 14, 10 ** 15 - 1)}_0_{-random.randint(10 ** 8, 10 ** 9 - 1)}'
            )
        upload_url = f'https://rupload.facebook.com/messenger_audio/{iid}'
        basename = os.path.basename(file_path)
        safe_name = ''.join(ch if ord(ch) < 128 else '_' for ch in basename)
        headers_up = {'User-Agent': str(ck['User-Agent']),
            'Accept-Encoding': 'zstd', 'accept-language': 'ar-EG, en-US',
            'authorization': token, 'priority': 'u=6, i', 'x-fb-client-ip':
            'True', 'x-fb-friendly-name': 'undefined:media-upload',
            'x-fb-server-cluster': 'True', 'x-mid': str(mid), 'audio_type':
            'FILE_ATTACHMENT', 'x-fb-http-engine': 'MNS'}
        r1 = requests.get(upload_url, headers=headers_up)
        if r1.status_code != 200:
            return False
        offset = r1.json().get('offset', 0)
        rem = size - offset
        if rem <= 0:
            return False
        headers_up.update({'offset': str(offset), 'x-entity-length': str(
            rem), 'x-entity-name': safe_name, 'x-entity-type': 'audio/mp4'})
        with open(file_path, 'rb') as f:
            f.seek(offset)
            data = f.read()
        r2 = requests.post(upload_url, data=data, headers=headers_up)
        if r2.status_code != 200 or 'media_id' not in r2.text:
            return False
        media_id = r2.json()['media_id']
        send_url = (
            'https://i.instagram.com/api/v1/direct_v2/threads/broadcast/voice_attachment/'
            )
        payload = {'action': 'send_item', 'recipient_users':
            f'[[{user_id}]]', 'attachment_fbid': str(media_id),
            'client_context': str(uuid.uuid4().int)[:19], 'device_id': str(
            uuid.uuid4()), 'mutation_token': str(uuid.uuid4().int)[:19],
            'offline_threading_id': str(uuid.uuid4().int)[:19], 'waveform':
            '[0,0,0,0,0,0,0,0,0,0]', 'waveform_sampling_frequency_hz': '10',
            'is_shh_mode': '0', 'send_attribution': 'inbox',
            'btt_dual_send': 'false', 'is_ae_dual_send': 'false',
            'upload_id': str(int(datetime.datetime.now().timestamp() * 1000
            )), '_uuid': str(uuid.uuid4())}
        headers_send = {'User-Agent': headers_up['User-Agent'],
            'accept-language': headers_up['accept-language'],
            'authorization': token, 'x-ig-app-id': '567067343352427',
            'x-ig-device-id': payload['_uuid'], 'x-ig-timezone-offset': str
            ((datetime.datetime.now().astimezone().utcoffset() or datetime.
            timedelta()).seconds)}
        r3 = requests.post(send_url, data=payload, headers=headers_send)
        return r3.text

    def img_message(self, user_target, img_path):
        if not os.path.isfile(img_path):
            return False, f'Image not found at path: {img_path}'
        ck = self.ck
        if ck == False:
            return False, ck
        id = userid(self.username, self.password, user_target)
        iid = (
            f'{random.randint(10 ** 14, 10 ** 15 - 1)}_0_{-random.randint(10 ** 8, 10 ** 9 - 1)}'
            )
        url = f'https://rupload.facebook.com/messenger_image/{iid}'
        with open(img_path, 'rb') as f:
            payload = f.read()
        headers = {'User-Agent': str(ck['User-Agent']), 'Content-Type':
            'application/octet-stream', 'x-entity-length': str(len(payload)
            ), 'x-entity-name': str(iid), 'x-entity-type': 'image/jpeg',
            'x-ig-salt-ids': '51052545', 'image_type': 'FILE_ATTACHMENT',
            'offset': '0', 'priority': 'u=6, i', 'accept-language':
            'ar-EG, en-US', 'authorization': str(ck['token']), 'x-mid': str
            (ck['mid']), 'ig-u-ds-user-id': str(ck['ds_user_id']),
            'ig-intended-user-id': str(ck['ds_user_id']),
            'x-fb-http-engine': 'Liger', 'x-fb-client-ip': 'True',
            'x-fb-server-cluster': 'True'}
        r = requests.post(url, data=payload, headers=headers)
        if r.status_code == 200:
            media_id = r.json().get('media_id')
            if not media_id:
                return False, 'Failed to get media_id from response'
            uu = str(uuid.uuid4().int)[:19]
            url = (
                'https://i.instagram.com/api/v1/direct_v2/threads/broadcast/photo_attachment/'
                )
            payload = {'action': 'send_item', 'is_x_transport_forward':
                'false', 'is_shh_mode': '0', 'recipient_users': f'[[{id}]]',
                'send_attribution': 'inbox', 'client_context': str(uu),
                'attachment_fbid': str(media_id), 'device_id':
                'android-cfc948366e9e83d2', 'mutation_token': str(uu),
                '_uuid': str(uuid.uuid4()), 'allow_full_aspect_ratio':
                'true', 'offline_threading_id': str(uu)}
            headers = {'User-Agent': str(ck['User-Agent']),
                'x-ig-www-claim': str(ck['claim']), 'x-bloks-is-layout-rtl':
                'true', 'x-ig-device-id':
                'e6ddb56b-a663-478c-ada8-9af7e2e9039b',
                'x-ig-family-device-id':
                '20c62d28-65ee-4533-ba6f-52155545866d', 'x-ig-android-id':
                'android-cfc948366e9e83d2', 'x-ig-timezone-offset': str((
                datetime.datetime.now().astimezone().utcoffset() or
                datetime.timedelta()).seconds), 'x-ig-app-id':
                '567067343352427', 'priority': 'u=3', 'accept-language':
                'ar-EG, en-US', 'authorization': str(ck['token']), 'x-mid':
                str(ck['mid']), 'ig-u-ds-user-id': str(ck['ds_user_id']),
                'ig-intended-user-id': str(ck['ds_user_id'])}
            response = requests.post(url, data=payload, headers=headers)
            if response.json().get('status') == 'ok':
                return True, response.json()
            else:
                return False, response.json()
        else:
            return False, r.text

    def video_message(self, user_target, video_path):
        ck = self.ck
        if ck == False:
            return False, ck
        id = userid(self.username, self.password, user_target)
        if not os.path.isfile(video_path):
            return False, f'Video not found at path: {video_path}'
        file_size = os.path.getsize(video_path)
        current_ms = int(time.time() * 1000)
        random_part = uuid.uuid4().hex[:32]
        entity_name = (
            f'{random_part}-0-{file_size}-{current_ms}-{current_ms + 606}')
        url = f'https://rupload.facebook.com/messenger_video/{entity_name}'
        with open(video_path, 'rb') as f:
            payload = f.read()
        headers = {'User-Agent': str(ck['User-Agent']), 'Content-Type':
            'application/octet-stream', 'x-entity-length': str(file_size),
            'x-entity-name': entity_name, 'x-entity-type': 'video/mp4',
            'segment-start-offset': '0', 'video_type': 'FILE_ATTACHMENT',
            'x_fb_video_waterfall_id': f'{uuid.uuid4().hex[:15]}_Mixed_0',
            'segment-type': '3', 'offset': '0', 'priority': 'u=6, i',
            'accept-language': 'ar-EG, en-US', 'authorization': str(ck[
            'token']), 'x-mid': str(ck['mid']), 'ig-u-ds-user-id': str(ck[
            'ds_user_id']), 'ig-intended-user-id': str(ck['ds_user_id']),
            'x-fb-http-engine': 'Liger', 'x-fb-client-ip': 'True',
            'x-fb-server-cluster': 'True'}
        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 200:
            media_id = response.json()['media_id']
            uu = str(uuid.uuid4().int)[:19]
            url = (
                'https://i.instagram.com/api/v1/direct_v2/threads/broadcast/video_attachment/'
                )
            payload = {'action': 'send_item', 'is_x_transport_forward':
                'false', 'is_shh_mode': '0', 'recipient_users': f'[[{id}]]',
                'send_attribution': 'inbox', 'client_context': str(uu),
                'attachment_fbid': str(media_id), 'video_result': str(
                media_id), 'device_id': 'android-cfc948366e9e83d2',
                'mutation_token': str(uu), '_uuid': str(uuid.uuid4()),
                'offline_threading_id': str(uu)}
            headers = {'User-Agent': str(ck['User-Agent']),
                'x-ig-www-claim': str(ck['claim']), 'x-ig-timezone-offset':
                str((datetime.datetime.now().astimezone().utcoffset() or
                datetime.timedelta()).seconds), 'x-ig-app-id':
                '567067343352427', 'priority': 'u=3', 'accept-language':
                'ar-EG, en-US', 'authorization': str(ck['token']), 'x-mid':
                str(ck['mid']), 'ig-u-ds-user-id': str(ck['ds_user_id']),
                'ig-intended-user-id': str(ck['ds_user_id'])}
            response = requests.post(url, data=payload, headers=headers)
            if response.ok == True:
                return True, response.json()
        else:
            return False, response.text

    def like(self, url_post):
        ids = media_id(url_post)
        ck = self.ck
        if ck == False:
            return False, ck
        url = f'https://i.instagram.com/api/v1/media/{ids}/like/'
        payload_dict = {'media_id': str(ids), '_uid': str(ck['ds_user_id']),
            '_uuid': str(uuid.uuid4()), 'container_module':
            'feed_contextual_chain'}
        data = {'signed_body': f'SIGNATURE.{json.dumps(payload_dict)}', 'd':
            '0'}
        headers = {'User-Agent': str(ck['User-Agent']),
            'x-ig-timezone-offset': str((datetime.datetime.now().astimezone
            ().utcoffset() or datetime.timedelta()).seconds), 'x-ig-app-id':
            '567067343352427', 'authorization': str(ck['token'])}
        response = requests.post(url, data=data, headers=headers)
        return response.json()

    def comment(self, url_post, txt):
        ids = media_id(url_post)
        ck = self.ck
        if ck == False:
            return False, ck
        url = f'https://i.instagram.com/api/v1/media/{ids}/comment/'
        headers = {'User-Agent': str(ck['User-Agent']),
            'x-ig-timezone-offset': str((datetime.datetime.now().astimezone
            ().utcoffset() or datetime.timedelta()).seconds), 'x-ig-app-id':
            '567067343352427', 'authorization': str(ck['token']), 'x-mid':
            str(ck['mid']), 'ig-u-ds-user-id': str(ck['ds_user_id']),
            'ig-intended-user-id': str(ck['ds_user_id'])}
        payload = {'comment_text': str(txt), '_uid': str(ck['ds_user_id']),
            '_uuid': str(), 'idempotence_token': str(uuid.uuid4())}
        data = {'signed_body': f'SIGNATURE.{json.dumps(payload)}'}
        r = requests.post(url, headers=headers, data=data)
        if r.json().get('status') == 'ok' and 'comment' in r.json():
            return True, r.json()
        else:
            return r.text

    def follow(self, user_target):
        ck = self.ck
        if ck == False:
            return False, ck
        id = userid(self.username, self.password, user_target)
        url = f'https://i.instagram.com/api/v1/friendships/create/{id}/'
        headers = {'User-Agent': str(ck['User-Agent']),
            'x-ig-timezone-offset': str((datetime.datetime.now().astimezone
            ().utcoffset() or datetime.timedelta()).seconds), 'x-ig-app-id':
            '567067343352427', 'authorization': str(ck['token']), 'x-mid':
            str(ck['mid']), 'ig-u-ds-user-id': str(ck['ds_user_id']),
            'ig-intended-user-id': str(ck['ds_user_id'])}
        payload = {'user_id': str(id), '_uid': str(ck['ds_user_id']),
            '_uuid': str(uuid.uuid4())}
        data = {'signed_body': f'SIGNATURE.{json.dumps(payload)}'}
        response = requests.post(url, headers=headers, data=data).json()
        if response.get('friendship_status', {}).get('following') == True:
            return True, response
        else:
            return False, response

    def unfollow(self, user_target):
        ck = self.ck
        if ck == False:
            return False, ck
        id = userid(self.username, self.password, user_target)
        url = f'https://i.instagram.com/api/v1/friendships/destroy/{id}/'
        payload = {'user_id': str(id), '_uid': str(ck['ds_user_id']),
            '_uuid': str(uuid.uuid4())}
        data = {'signed_body': f'SIGNATURE.{json.dumps(payload)}'}
        headers = {'User-Agent': str(ck['User-Agent']),
            'x-ig-timezone-offset': str((datetime.datetime.now().astimezone
            ().utcoffset() or datetime.timedelta()).seconds), 'x-ig-app-id':
            '567067343352427', 'authorization': str(ck['token']), 'x-mid':
            str(ck['mid']), 'ig-u-ds-user-id': str(ck['ds_user_id']),
            'ig-intended-user-id': str(ck['ds_user_id'])}
        r = requests.post(url, data=payload, headers=headers).json()
        if r['status'] == 'ok' and not r['friendship_status']['following']:
            return True, r
        else:
            return False, r

    def create_note(self, txt):
        ck = self.ck
        if ck == False:
            return False, ck
        url = 'https://i.instagram.com/api/v1/notes/create_note/'
        payload = {'note_style': '0', 'text': str(txt), '_uuid': str(uuid.
            uuid4()), 'audience': '0'}
        headers = {'User-Agent': str(ck['User-Agent']), 'authorization':
            str(ck['token']), 'ig-intended-user-id': str(ck['ds_user_id']),
            'ig-u-ds-user-id': str(ck['ds_user_id']), 'x-ig-app-id':
            '567067343352427', 'x-ig-timezone-offset': str((datetime.
            datetime.now().astimezone().utcoffset() or datetime.timedelta()
            ).seconds)}
        response = requests.post(url, data=payload, headers=headers)
        if response.json().get('status') == 'ok':
            return True, response.json()
        else:
            return False, response.text

    def story(self, file_path):
        ck = self.ck
        if ck == False:
            return False, ck
        iid = (
            f'{random.randint(10 ** 14, 10 ** 15 - 1)}_0_{-random.randint(10 ** 8, 10 ** 9 - 1)}'
            )
        url = f'https://i.instagram.com/rupload_igphoto/{iid}'
        allowed_extensions = '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'
        if not file_path.lower().endswith(allowed_extensions):
            return False, 'Only images are supported'
        with open(file_path, 'rb') as f:
            payload = f.read()
        upload_id = str(random.randint(10 ** 16, 10 ** 17 - 1))
        rupload_params = {'upload_id': upload_id, 'media_type': '1',
            'retry_context': json.dumps({'num_reupload': 0,
            'num_step_auto_retry': 0, 'num_step_manual_retry': 0}),
            'image_compression': json.dumps({'lib_name': 'moz',
            'lib_version': '3.1.m', 'quality': '70', 'original_width': 1080,
            'original_height': 1920}), 'xsharing_user_ids': '[]'}
        headers = {'User-Agent': str(ck['User-Agent']), 'Content-Type':
            'application/octet-stream', 'x-entity-length': str(len(payload)
            ), 'x-entity-name': iid, 'x-entity-type': 'image/jpeg',
            'offset': '0', 'x-instagram-rupload-params': json.dumps(
            rupload_params), 'authorization': str(ck['token']),
            'x-ig-app-id': '567067343352427'}
        r = requests.post(url, data=payload, headers=headers)
        if 'upload_id' in r.text:
            upload_id = r.json()['upload_id']
            tm = int(time.time())
            tt = tm - random.randint(2, 5)
            uiu = 'https://i.instagram.com/api/v1/media/configure_to_story/'
            headers = {'User-Agent': str(ck['User-Agent']), 'retry_context':
                '{"num_reupload":0,"num_step_auto_retry":0,"num_step_manual_retry":0}'
                , 'x-ig-app-id': '567067343352427', 'authorization': str(ck
                ['token']), 'x-mid': str(ck['mid'])}
            payload = {'supported_capabilities_new': [{'name':
                'SUPPORTED_SDK_VERSIONS', 'value': '119.0,120.0,121.0'}, {
                'name': 'FACE_TRACKER_VERSION', 'value': '14'}, {'name':
                'COMPRESSION', 'value': 'ETC2_COMPRESSION'}],
                'original_media_type': '1', 'upload_id': str(upload_id),
                '_uuid': str(uuid.uuid4()), '_uid': str(ck['ds_user_id']),
                'source_type': '4', 'configure_mode': '1',
                'timezone_offset': str((datetime.datetime.now().astimezone(
                ).utcoffset() or datetime.timedelta()).seconds),
                'client_timestamp': str(tm), 'client_shared_at': str(tt),
                'creation_surface': 'camera', 'camera_position': 'unknown',
                'camera_entry_point': '71'}
            data = {'signed_body':
                f"SIGNATURE.{json.dumps(payload, separators=(',', ':'))}"}
            rr = requests.post(uiu, headers=headers, data=data).json()
            if rr.get('status') == 'ok' and 'media' in rr and 'pk' in rr[
                'media']:
                return True, rr
            else:
                return False, rr
        else:
            return False, r.text

    def post_img(self, file_path, txt=None):
        if txt is None:
            txt = '.'
        ck = self.ck
        if ck is False:
            return False, ck
        allowed_extensions = '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'
        if not file_path.lower().endswith(allowed_extensions):
            return (False,
                'Unsupported image format. Allowed: jpg, jpeg, png, gif, bmp, webp'
                )
        mime_type = mimetypes.guess_type(file_path)[0]
        if not mime_type or not mime_type.startswith('image/'):
            return False, 'Could not detect valid image MIME type'
        try:
            with open(file_path, 'rb') as f:
                payload = f.read()
        except Exception as e:
            return False, f'Error reading file: {str(e)}'
        upload_id = str(random.randint(10 ** 14, 10 ** 15 - 1))
        iid = f'{upload_id}_0_{-random.randint(10 ** 8, 10 ** 9 - 1)}'
        url = f'https://i.instagram.com/rupload_igphoto/{iid}'
        rupload_params = {'upload_id': upload_id, 'media_type': '1',
            'retry_context': json.dumps({'num_reupload': 0,
            'num_step_auto_retry': 0, 'num_step_manual_retry': 0}),
            'image_compression': json.dumps({'lib_name': 'moz',
            'lib_version': '3.1.m', 'quality': '75', 'original_width': 1080,
            'original_height': 1920}), 'xsharing_user_ids': '[]'}
        headers = {'User-Agent': str(ck['User-Agent']), 'Content-Type':
            'application/octet-stream', 'x-entity-length': str(len(payload)
            ), 'x-entity-name': iid, 'x-entity-type': mime_type, 'offset':
            '0', 'x-instagram-rupload-params': json.dumps(rupload_params),
            'x-ig-app-id': '567067343352427', 'authorization': str(ck[
            'token']), 'x-mid': str(ck['mid'])}
        rr = requests.post(url, data=payload, headers=headers)
        if rr.status_code == 200:
            upload_id = rr.json()['upload_id']
            url = 'https://i.instagram.com/api/v1/media/configure/'
            payload_data = {'upload_id': str(upload_id), 'caption': str(txt
                ), 'timezone_offset': str((datetime.datetime.now().
                astimezone().utcoffset() or datetime.timedelta()).seconds),
                'source_type': '4', 'device': {'manufacturer': 'Xiaomi',
                'model': 'M2102J20SG', 'android_version': 31,
                'android_release': '12'}, 'edits': {'crop_original_size': [
                832.0, 1248.0], 'crop_center': [0.0, -0.33333334],
                'crop_zoom': 1.5}, 'extra': {'source_width': 832,
                'source_height': 1248}}
            payload = {'signed_body': f'SIGNATURE.{json.dumps(payload_data)}'}
            headers = {'User-Agent': str(ck['User-Agent']), 'retry_context':
                '{"num_reupload":0,"num_step_auto_retry":0,"num_step_manual_retry":0}'
                , 'x-ig-app-id': '567067343352427', 'authorization': str(ck
                ['token']), 'x-mid': str(ck['mid'])}
            rrr = requests.post(url, data=payload, headers=headers)
            try:
                cond1 = rrr.json().get('integrity_review_decision'
                    ) == 'pending'
                cond2 = rrr.json().get('caption', {}).get('status') == 'Active'
                media = rrr.json().get('media', {})
                cond3 = 'pk' in media and 'id' in media
                if cond1 or cond2 or cond3:
                    return True, rrr.json()
                else:
                    return False, rrr.text
            except Exception as e:
                return str(e)
        else:
            return rr.text

    def edit_profile(self, new_username=None, new_full_name=None, new_bio=None
        ):
        ck = self.ck
        if ck is False:
            return False, ck
        headers = {'User-Agent': str(ck['User-Agent']), 'x-ig-app-id':
            '567067343352427', 'authorization': str(ck['token']), 'x-mid':
            str(ck['mid'])}
        url = 'https://i.instagram.com/api/v1/accounts/current_user/?edit=true'
        response = requests.get(url, headers=headers)
        rr = response.json()['user']
        if new_username:
            check_payload = {'username': new_username, '_uid':
                '73208098997', '_uuid': 'e6ddb56b-a663-478c-ada8-9af7e2e9039b'}
            check_url = 'https://i.instagram.com/api/v1/users/check_username/'
            data = {'signed_body': f'SIGNATURE.{json.dumps(check_payload)}'}
            check_response = requests.post(check_url, data=data, headers=
                headers).json()
            if not check_response.get('available'):
                return check_response
        payload = {'primary_profile_link_type': str(rr[
            'primary_profile_link_type']), 'external_url': str(rr[
            'external_url']), 'phone_number': str(rr['phone_number']),
            'username': new_username if new_username else str(rr['username'
            ]), 'show_fb_link_on_profile': str(rr['show_fb_link_on_profile'
            ]).lower(), 'first_name': new_full_name if new_full_name else
            rr['full_name'], '_uid': str(ck['ds_user_id']), 'biography': 
            new_bio if new_bio else rr['biography'], '_uuid': str(uuid.
            uuid4()), 'email': str(rr['email'])}
        edit_url = 'https://i.instagram.com/api/v1/accounts/edit_profile/'
        data = {'signed_body': f'SIGNATURE.{json.dumps(payload)}'}
        edit_response = requests.post(edit_url, data=data, headers=headers)
        try:
            return edit_response.json()
        except:
            return edit_response.text

    def edit_profile_img(self, image_path):
        ck = self.ck
        if ck is False:
            return False, ck
        upload_id = str(int(time.time() * 1000))
        mime_type, _ = mimetypes.guess_type(image_path)
        image_size = os.path.getsize(image_path)
        entity_name = f'{upload_id}_0_{-random.randint(10 ** 8, 10 ** 9 - 1)}'
        rupload_params = {'upload_id': upload_id, 'media_type': '1',
            'image_compression': json.dumps({'lib_name': 'moz',
            'lib_version': '3.1.m', 'quality': '77'})}
        hh = {'User-Agent': str(ck['User-Agent']), 'Content-Type':
            'application/octet-stream', 'x-entity-length': str(image_size),
            'x-entity-name': entity_name, 'x-instagram-rupload-params':
            json.dumps(rupload_params), 'x-entity-type': mime_type or
            'image/jpeg', 'offset': '0', 'authorization': str(ck['token']),
            'x-mid': str(ck['mid'])}
        url = f'https://i.instagram.com/rupload_igphoto/{entity_name}'
        with open(image_path, 'rb') as f:
            image_data = f.read()
        ro = requests.post(url, data=image_data, headers=hh)
        if ro.status_code == 200:
            upload_id = ro.json()['upload_id']
            url = (
                'https://i.instagram.com/api/v1/accounts/change_profile_picture/'
                )
            payload = {'_uuid': str(uuid.uuid4()), 'use_fbuploader': 'true',
                'upload_id': str(upload_id)}
            headers = {'User-Agent': str(ck['User-Agent']), 'x-ig-app-id':
                '567067343352427', 'authorization': str(ck['token']),
                'x-mid': str(ck['mid'])}
            rr = requests.post(url, data=payload, headers=headers)
            if rr.status_code == 200 and rr.json().get('status') == 'ok':
                return True, rr.json()
            else:
                return False, rr.text
        else:
            return False, ro.text

    def _year(self, user_id):
        ranges = [
            (1, 1278889, 2010), (1279000, 17750000, 2011), (17750001, 279760000, 2012),
            (279760001, 900990000, 2013), (900990001, 1629010000, 2014),
            (1629010001, 2369359761, 2015), (2369359762, 4239516754, 2016),
            (4239516755, 6345108209, 2017), (6345108210, 10016232395, 2018),
            (10016232396, 27238602159, 2019), (27238602160, 43464475395, 2020),
            (43464475396, 50289297647, 2021), (50289297648, 57464707082, 2022),
            (57464707083, 63313426938, 2023)
        ]
        for start, end, year in ranges:
            if start <= user_id <= end:
                return year
        return '2024 or 2025'
    

    def get_info_A(self, user_target):
        ck = self.ck
        if ck == False:
            return False, ck
    
        idf = userid(self.username, self.password, user_target)
        url = f'https://i.instagram.com/api/v1/users/{idf}/info/?entry_point=profile&from_module=profile'
        headers = {
            'User-Agent': str(ck['User-Agent']),
            'x-ig-app-id': '567067343352427',
            'authorization': str(ck['token']),
            'x-mid': str(ck['mid'])
        }
    
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            user = response.json().get('user', {})
            ids = user.get('pk', '')
            return {
                'username': user.get('username', ''),
                'full_name': user.get('full_name', ''),
                'biography': user.get('biography', ''),
                'is_private': user.get('is_private', False),
                'is_verified': user.get('is_verified', False),
                'followers': user.get('follower_count', 0),
                'following': user.get('following_count', 0),
                'posts': user.get('media_count', 0),
                'img': user.get('hd_profile_pic_url_info', {}).get('url', ''),
                'user_id': ids,
                'creation_date': self._year(int(ids))
            }
        else:
            return {
                'username': 'erorr',
                'full_name': '',
                'biography': '',
                'is_private': '',
                'is_verified': '',
                'followers': '',
                'following': '',
                'posts': '',
                'img': '',
                'user_id': '',
                'creation_date': ''
            }
    

    def get_info_B(self, username):
        url = f'https://api.digitalbyte.cc/instagram/tucktools2.com/{username}'
        headers = {'user-agent': str(user_agent.generate_user_agent())}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('status'):
                    user = data
                    return {
                        'username': user.get('username', ''),
                        'full_name': user.get('user_fullname', ''),
                        'biography': user.get('user_description', ''),
                        'is_private': user.get('is_private', False),
                        'is_verified': user.get('is_verified', False),
                        'followers': user.get('user_followers', 0),
                        'following': user.get('user_following', 0),
                        'posts': user.get('total_posts', 0),
                        'img': user.get('user_profile_pic', ''),
                        'user_id': '',
                        'creation_date': '',
                        'Erorr': False
                    }
        except Exception as e:
            return {
                'username': 'erorr',
                'full_name': '',
                'biography': '',
                'is_private': '',
                'is_verified': '',
                'followers': '',
                'following': '',
                'posts': '',
                'img': '',
                'user_id': '',
                'creation_date': '',
                'Erorr': str(e)
            }


    def download_story(self, user_target):
        ck = self.ck
        if ck == False:
            return False, ck
        ids = userid(self.username, self.password, user_target)
        url = f'https://i.instagram.com/api/v1/feed/user/{ids}/story/'
        h = {'User-Agent': ck['User-Agent'], 'authorization': ck['token'],
            'ig-intended-user-id': ck['ds_user_id'], 'ig-u-ds-user-id': ck[
            'ds_user_id'], 'priority': 'u=3', 'x-ig-app-id':
            '567067343352427', 'x-ig-timezone-offset': str((datetime.
            datetime.now().astimezone().utcoffset() or datetime.timedelta()
            ).seconds), 'x-ig-www-claim': ck['claim'], 'x-mid': ck['mid'],
            'x-pigeon-rawclienttime': f'{time.time():.3f}'}
        r = requests.get(url, headers=h)
        urls = []
        if r.ok:
            for i in r.json().get('reel', {}).get('items', []):
                key = ('video_versions' if 'video_versions' in i else
                    'image_versions2')
                cand = i.get(key, {}).get('candidates', []
                    ) if key == 'image_versions2' else i.get(key, [])
                if cand:
                    urls.append(cand[0]['url'])
            return True, urls
        return False, r.text

    def download_story_b(self, user_target):
        url = 'https://anon-viewer.com/content.php'
        hea = {'user-agent': str(user_agent.generate_user_agent())}
        pa = {'url': str(user_target), 'method': 'allstories'}
        if requests.get(url, params=pa, headers=hea).json()['status'
            ] == 'error':
            r = False
        else:
            r = html.unescape(json.loads(requests.get(url, params=pa,
                headers=hea).text).get('html', ''))
            return re.findall(
                '(?:<source\\s+src=|<img\\s+src=)"([^"]+\\.(?:mp4|jpg|jpeg|png|webp|gif)[^"]*)"'
                , r, re.IGNORECASE)

    def download_posts(self, url_post):
        ck = self.ck
        if ck == False:
            return False, ck
        mids = media_id(url_post)
        if not mids:
            return []
        url = f'https://i.instagram.com/api/v1/media/{mids}/info/'
        h = {'User-Agent': ck['User-Agent'], 'Authorization': ck['token']}
        resp = requests.get(url, headers=h).json()
        if resp.get('status') != 'ok':
            return []
        items = resp.get('items', [])
        links = []
        if items:
            m = items[0]
            if m.get('media_type') == 8 and 'carousel_media' in m:
                for c in m['carousel_media']:
                    if c.get('media_type') == 1:
                        links.append(c['image_versions2']['candidates'][0][
                            'url'])
                    elif c.get('media_type') == 2:
                        links.append(c['video_versions'][0]['url'])
            elif m.get('media_type') == 1:
                links.append(m['image_versions2']['candidates'][0]['url'])
            elif m.get('media_type') == 2:
                links.append(m['video_versions'][0]['url'])
        return links

    def get_messages(self) ->dict:
        sss = requests.Session()
        ck = self.ck
        if not ck:
            return False, ck
        url = 'https://i.instagram.com/api/v1/direct_v2/inbox/'
        headers = {'User-Agent': str(ck['User-Agent']), 'Authorization':
            str(ck['token']), 'x-ig-app-id': '567067343352427'}
        response = sss.get(url, headers=headers)
        data = response.json()
        threads = data.get('inbox', {}).get('threads', [])
        if not threads:
            return {}
        last_thread = threads[0]
        users = last_thread.get('users', [])
        user_name = users[0].get('username', 'unknown_user'
            ) if users else 'unknown_user'
        last_msg = last_thread.get('last_permanent_item', {})
        msg_type = last_msg.get('item_type')
        if msg_type == 'text':
            message = last_msg.get('text', '')
        elif msg_type == 'media_share':
            message = last_msg.get('media_share', {}).get('code',
                'shared_media')
        elif msg_type == 'link':
            message = last_msg.get('link', {}).get('text', 'link_sent')
        elif msg_type == 'voice_media':
            message = '[Voice Message]'
        elif msg_type == 'raven_media':
            message = '[Disappearing Media]'
        elif msg_type == 'animated_media':
            message = '[GIF]'
        elif msg_type == 'media':
            media = last_msg.get('media', {})
            image_versions = media.get('image_versions2', {}).get('candidates',
                [])
            message = image_versions[0].get('url', '[Photo]'
                ) if image_versions else '[Media]'
        elif msg_type == 'action_log':
            message = last_msg.get('action_log', {}).get('description',
                '[action_log]')
        else:
            message = f'[{msg_type}]'
        return {'username': user_name, 'message': message}

    def get_inbox_request(self):
        ck = self.ck
        if ck == False:
            return False, ck
        url = (
            'https://i.instagram.com/api/v1/direct_v2/pending_inbox_streaming/?visual_message_return_type=unseen&thread_batch_size=5&thread_limit=20&thread_message_limit=1&persistentBadging=true')
        headers = {'User-Agent': str(ck['User-Agent']), 'x-ig-app-id':
            '567067343352427', 'authorization': str(ck['token'])}
        res = requests.get(url, headers=headers)
        m = re.search('"json_response":"(.*?)","status"', res.text, re.DOTALL)
        if not m:
            return 'no_message'
        raw = json.loads(f'"{m.group(1)}"')
        data = json.loads(raw)
        threads = data.get('inbox', {}).get('threads', [])
        if not threads:
            return 'no_message'
        t = threads[0]
        u = t.get('users', [{}])[0]
        i = t.get('items', [])
        msg = i[-1] if i else {}
        item_type = msg.get('item_type', '')
        message = msg.get('text') or msg.get('reel_share', {}).get('text', ''
            ) or f'[{item_type}]'
        return {'full_name': u.get('full_name', ''), 'username': u.get(
            'username', ''), 'message': message}
            
            
            

