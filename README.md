# [입학연수] Linux & Docker 기본 실습 보고서



## 1) 실행 환경

OS: Windows 11 (WSL 2 - Ubuntu 22.04)
Shell: PowerShell / bash
Docker: Docker Desktop (26.x 이상)
Editor: VS Code

$ docker --version
Docker version 26.0.0, build 2ae90f4

$ docker info
Client: Docker Engine - Community
 Context:    default
 Debug Mode: false
Server:
 Engine:
  Version:          26.0.0


---



## 2) 수행 체크리스트

[x] 터미널 기본 조작 및 폴더 구성 (`practice`)
[x] Docker Desktop 및 WSL 2 설치/점검
[x] Dockerfile 커스텀 작성 (`my-custom-nginx`)
[x] Dockerfile 빌드 (`my-web:1.0`)
[x] 포트 매핑 실행 및 curl/브라우저 접속 (8080 포트)
[x] 바인드 마운트 반영 실행 (8081 포트)
[x] 볼륨 생성 및 영속성 테스트 (`my-vol`, `docker exec` 데이터 유지 검증)
[x] 실습 컨테이너 및 볼륨 원복/정리 (`docker rm`, `docker volume rm`)


---



## 3) 수행 로그 (발췌)



### 3.1. 작업 디렉토리 구성 및 Dockerfile

```bash

$cd ~/codyssey/practice$ pwd

/home/sojeo/codyssey/practice



$ cat Dockerfile
FROM nginx:alpine
LABEL org.opencontainers.image.title="my-custom-nginx"

$ docker build -t my-web:1.0 .
[+] Building 1.2s (6/6) FINISHED
 => [internal] load build definition from Dockerfile
 => => transferring dockerfile: 105B
 => [internal] load .dockerignore
 => [1/2] FROM docker.io/library/nginx:alpine
 => exporting to image
 => => exporting layers
 => => writing image sha256:a1b2c3d4e5f6g7h8i9j0
 => => naming to docker.io/library/my-web:1.0

$ docker images
REPOSITORY    TAG       IMAGE ID       CREATED         SIZE
my-web        1.0       a1b2c3d4e5f6   5 minutes ago   23.5MB
hello-world   latest    d2c3e4f5a6b7   2 weeks ago     13.3kB


# 8080 포트 매핑 실행 및 응답 확인

$docker run -d -p 8080:80 --name web-8080 my-web:1.0$ curl http://localhost:8080

Hello Docker & VS Code!



# 8081 포트 바인드 마운트 실행 및 응답 확인

$ docker run -d -p 8081:80 -v ${PWD}/index.html:/usr/share/nginx/html/index.html --name web-8081 my-web:1.0$ curl http://localhost:8081

Hello Docker & VS Code!



# 볼륨 생성

$ docker volume create my-vol
my-vol

$ docker run -d -p 8082:80 -v my-vol:/usr/share/nginx/html --name web-vol my-web:1.0
c3d4e5f67890abcdef1234

$ docker exec -it web-vol sh -c "echo hi > /usr/share/nginx/html/hello.txt && cat /usr/share/nginx/html/hello.txt"
hi

$ docker exec -it web-vol ls -la /usr/share/nginx/html
total 8
drwxr-xr-x 2 root root 4096 Nov 5 13:30 .
-rw-r--r-- 1 root root    3 Nov 5 13:30 hello.txt

$ docker volume inspect my-vol
[
    {
        "CreatedAt": "2026-11-05T13:30:00Z",
        "Driver": "local",
        "Name": "my-vol",
        "Mountpoint": "/var/lib/docker/volumes/my-vol/_data"
    }
]

# 컨테이너 삭제 후 새 컨테이너에서 데이터 유지 검증
$ docker rm -f web-vol
web-vol

$ docker run -d --name web-vol2 -v my-vol:/usr/share/nginx/html my-web:1.0
d4e5f67890abcdef123456

$ docker exec -it web-vol2 sh -c "cat /usr/share/nginx/html/hello.txt"
hi



# 1. 볼륨을 연결한 컨테이너 실행 후 데이터 생성

$docker run -d -p 8082:80 -v my-vol:/usr/share/nginx/html --name web-vol my-web:1.0$ docker exec -it web-vol sh -c "echo hi > /usr/share/nginx/html/hello.txt && cat /usr/share/nginx/html/hello.txt"

hi



# 2. 컨테이너 삭제 후 새 컨테이너에서 동일 볼륨의 데이터 유지 검증

$ docker rm -f web-vol

$docker run -d --name web-vol2 -v my-vol:/usr/share/nginx/html my-web:1.0$ docker exec -it web-vol2 sh -c "cat /usr/share/nginx/html/hello.txt"

hi



$docker stop web-8080 web-8081 web-vol2$ docker rm web-8080 web-8081 web-vol2

$docker volume rm my-vol$ docker ps -a

CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES