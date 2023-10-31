# VS Code - Remote tunnel 사용하기

JupyterLab은 강력한 도구이지만, 때로는 TextEditor만으로는 개발에 제한이 있을 수 있습니다. VS Code는 개발 환경을 더 풍부하게 만들어주며, Remote Tunnel을 통해 원격 서버 환경을 사용하여 개발할 수 있는 기능을 제공합니다. 이 문서에서는 VS Code의 Remote Tunnel을 Jupyter 플랫폼에 적용하는 방법을 설명합니다.

## JupyterLab(Qupyter)에서 Tunnel 생성하기

1. 먼저 VS Code CLI를 설치합니다. 다음 명령어를 사용하여 CLI를 다운로드하고 압축을 해제합니다:

```bash
curl -Lk 'https://code.visualstudio.com/sha/download?build=stable&os=cli-alpine-x64' --output vscode_cli.tar.gz
tar -xf vscode_cli.tar.gz
```

2. 다음으로, CLI를 실행합니다:

```bash
./code tunnel
```

3. 실행하면 <https://github.com/login/device> 에 접속해 인증하라는 메시지가 표시됩니다.

```text
*
* Visual Studio Code Server
*
* By using the software, you agree to
* the Visual Studio Code Server License Terms (https://aka.ms/vscode-server-license) and
* the Microsoft Privacy Statement (https://privacy.microsoft.com/en-US/privacystatement).
*
To grant access to the server, please log into https://github.com/login/device and use code 5A0B-2489
```

4. GitHub 인증을 완료하면 브라우저에서 접속할 수 있는 링크가 화면에 출력됩니다.

```text
Open this link in your browser https://vscode.dev/tunnel/jupyter-kghoon/home/jovyan/volatility-break

[2023-10-25 02:24:47] info [tunnels::connections::relay_tunnel_host] Opened new client on channel 2
[2023-10-25 02:24:47] info [russh::server] wrote id
[2023-10-25 02:24:47] info [russh::server] read other id
[2023-10-25 02:24:47] info [russh::server] session is running
[2023-10-25 02:24:48] info [rpc.0] Checking /home/jovyan/.vscode/cli/servers/Stable-f1b07bd25dfad64b0167beb15359ae573aecd2cc/log.txt and /home/jovyan/.vscode/cli/servers/Stable-f1b07bd25dfad64b0167beb15359ae573aecd2cc/pid.txt for a running server...
[2023-10-25 02:24:48] info [rpc.0] Starting server...
[2023-10-25 02:24:48] info [rpc.0] Server started
```

5. 터미널에 출력된 주소를 웹 브라우저에서 열어주세요.

## 로컬(PC)에 설치된 VS Code를 사용하여 접속하기

Dev Containers extension을 사용하면 로컬에 설치 된 VS code를 사용해 위에서 생성한 터널에 접근할 수 있습니다.

1. VS Code에 "Dev Containers" 확장 프로그램을 설치합니다.

2. 좌측하단 '원격 창 열기' 버튼을 클릭합니다.

3. 터널에 연결을 선택합니다.

4. 목록에 위에서 설정한 tunnel이 나타나면 선택합니다.

## 맺음말

지금까지 VS code remote tuunel을 JupyterLab에 설치하고 설정하는 방법을 설명했습니다. 이 도구를 사용하여 더 나은 개발 경험을 즐기시길 바랍니다. VS Code의 Remote Tunnel을 통해 JupyterLab에서 더 효율적으로 개발할 수 있게 되었습니다.

## 참고

- Developing with Remote Tunnels - <https://code.visualstudio.com/docs/remote/tunnels>
