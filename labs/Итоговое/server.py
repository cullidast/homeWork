import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

TASKS_FILE = "tasks.txt"

# Глобальная переменная для хранения задач в памяти.
tasks = []


def load_tasks():
    """Загружает список задач из файла, если файл существует."""
    global tasks
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            try:
                tasks = json.load(f)
            except json.JSONDecodeError:
                tasks = []


def save_tasks():
    """Сохраняет список задач в файл."""
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def get_next_id():
    """Возвращает новый уникальный идентификатор задачи."""
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


class TodoHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """
        Обработка GET-запросов:
          - GET /tasks -> возвращает все задачи в JSON
        """
        parsed_path = urlparse(self.path)
        path_segments = parsed_path.path.strip("/").split("/")

        # GET /tasks
        if len(path_segments) == 1 and path_segments[0] == 'tasks':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()

            response_body = json.dumps(tasks, ensure_ascii=False)
            self.wfile.write(response_body.encode('utf-8'))
        else:
            # Если не удалось распарсить путь, отправляем 404
            self.send_error(404, "Not Found")

    def do_POST(self):
        """
        Обработка POST-запросов:
          1) POST /tasks
             - тело запроса: JSON {"title": "...", "priority": "..."}
             - возвращает созданную задачу {"id": ..., "title": "...", "priority": "...", "isDone": false}
          2) POST /tasks/<id>/complete
             - отмечает задачу выполненной, если существует
        """
        parsed_path = urlparse(self.path)
        path_segments = parsed_path.path.strip("/").split("/")

        if len(path_segments) == 1 and path_segments[0] == 'tasks':
            # POST /tasks — создаём новую задачу
            self.handle_create_task()
        elif len(path_segments) == 3 and path_segments[0] == 'tasks' and path_segments[2] == 'complete':
            # POST /tasks/<id>/complete — отметка о выполнении
            try:
                task_id = int(path_segments[1])
            except ValueError:
                self.send_error(400, "Invalid task ID")
                return

            self.handle_complete_task(task_id)
        else:
            self.send_error(404, "Not Found")

    def handle_create_task(self):
        """Обработка создания новой задачи (POST /tasks)."""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
            return

        title = data.get("title")
        priority = data.get("priority")

        if not title or not priority:
            self.send_error(400, "Missing 'title' or 'priority'")
            return

        new_task = {
            "id": get_next_id(),
            "title": title,
            "priority": priority,
            "isDone": False
        }
        tasks.append(new_task)
        save_tasks()

        # Формируем ответ
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()

        response_body = json.dumps(new_task, ensure_ascii=False)
        self.wfile.write(response_body.encode('utf-8'))

    def handle_complete_task(self, task_id):
        """Обработка отметки задачи как выполненной (POST /tasks/<id>/complete)."""
        for task in tasks:
            if task["id"] == task_id:
                task["isDone"] = True
                save_tasks()

                self.send_response(200)
                self.end_headers()
                return

        # Если задача не найдена
        self.send_error(404, "Task not found")


def run_server(host="127.0.0.1", port=8080):
    """Запускает HTTP-сервер."""
    load_tasks()  # Сначала загружаем сохранённые задачи
    server_address = (host, port)
    httpd = HTTPServer(server_address, TodoHTTPRequestHandler)
    print(f"Starting server on http://{host}:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("\nServer stopped.")


if __name__ == "__main__":
    run_server()
