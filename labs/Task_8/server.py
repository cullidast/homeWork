import os
import urllib.parse
import json
from requests import get, put
from http.server import BaseHTTPRequestHandler, HTTPServer


def run(handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, handler_class)
    try:
        print("Server running on http://localhost:8000")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close()


class HttpGetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Генерация HTML списка файлов
        def fname2html(fname):
            return f"""
                <li onclick="fetch('/upload', {{'method': 'POST', 'body': '{fname}'}})">
                    {fname}
                </li>
            """

        # Заголовок HTTP-ответа
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        # Формируем HTML с файлами из папки "pdfs"
        files_list_html = "\n".join(map(fname2html, os.listdir("pdfs")))
        html = f"""
            <html>
                <head>
                    <title>File Uploader</title>
                </head>
                <body>
                    <h1>Files in 'pdfs' folder</h1>
                    <ul>
                        {files_list_html}
                    </ul>
                </body>
            </html>
        """
        self.wfile.write(html.encode("utf-8"))

    def do_POST(self):
        # Получаем имя файла из POST-запроса
        content_len = int(self.headers.get('Content-Length'))
        fname = self.rfile.read(content_len).decode("utf-8")
        local_path = f"pdfs/{fname}"
        ya_path = f"Backup/{urllib.parse.quote(fname)}"

        # Получаем URL для загрузки
        resp = get(
            "https://cloud-api.yandex.net/v1/disk/resources/upload",
            headers={"Authorization": f"OAuth {OAUTH_TOKEN}"},
            params={"path": ya_path, "overwrite": "true"}
        )

        # Проверяем ответ и наличие ошибки
        if resp.status_code != 200:
            print("Failed to get upload URL:", resp.status_code, resp.text)
            self.send_response(500)
            self.end_headers()
            return

        # Получаем ссылку на асинхронную операцию
        upload_url = json.loads(resp.text)["href"]

        # Создаем папку на Диске, если ее нет
        resp = get(
            "https://cloud-api.yandex.net/v1/disk/resources",
            headers={"Authorization": f"OAuth {OAUTH_TOKEN}"},
            params={"path": "Backup"}
        )
        if resp.status_code == 404:  # Если папки нет, создаем ее
            resp = put(
                "https://cloud-api.yandex.net/v1/disk/resources",
                headers={"Authorization": f"OAuth {OAUTH_TOKEN}"},
                params={"path": "Backup"}
            )
            if resp.status_code != 201:
                print("Failed to create folder 'Backup':", resp.status_code, resp.text)
                self.send_response(500)
                self.end_headers()
                return

        # Загружаем файл асинхронно
        with open(local_path, 'rb') as f:
            upload_resp = put(upload_url, files={'file': f})

        # Проверяем код ответа
        if upload_resp.status_code == 202:
            # Операция началась успешно, получаем ссылку на отслеживание
            tracking_url = json.loads(upload_resp.text)["href"]
            print(f"File '{fname}' upload started. Tracking URL: {tracking_url}")
            self.send_response(202)
            self.end_headers()
            self.wfile.write(json.dumps({"tracking_url": tracking_url}).encode("utf-8"))
        else:
            print(f"Failed to start upload for file '{fname}':", upload_resp.status_code, upload_resp.text)
            self.send_response(500)
            self.end_headers()


if __name__ == "__main__":
    # Запрашиваем токен у пользователя
    OAUTH_TOKEN = input("Введите ваш OAuth токен Яндекс.Диска: ").strip()

    # Проверяем папку "pdfs"
    if not os.path.exists("pdfs"):
        os.makedirs("pdfs")
        print("Создана папка 'pdfs'. Поместите в нее файлы для загрузки.")

    # Запуск сервера
    run(handler_class=HttpGetHandler)
