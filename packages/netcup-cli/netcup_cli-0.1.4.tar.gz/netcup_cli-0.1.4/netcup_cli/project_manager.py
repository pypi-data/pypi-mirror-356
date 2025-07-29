import sqlite3
import os

class ProjectManager:
    def __init__(self, db_path):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self._init_db()

    def _init_db(self):
        c = self.conn.cursor()
        c.execute(
            "CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE)"
        )
        c.execute(
            "CREATE TABLE IF NOT EXISTS project_servers (project_id INTEGER, vserver_name TEXT, UNIQUE(project_id, vserver_name))"
        )
        self.conn.commit()

    def create_project(self, name):
        with self.conn:
            self.conn.execute("INSERT OR IGNORE INTO projects (name) VALUES (?)", (name,))

    def list_projects(self):
        c = self.conn.cursor()
        projects = []
        for pid, name in c.execute("SELECT id, name FROM projects ORDER BY name").fetchall():
            servers = [row[0] for row in c.execute(
                "SELECT vserver_name FROM project_servers WHERE project_id=? ORDER BY vserver_name",
                (pid,),
            ).fetchall()]
            projects.append({"name": name, "servers": servers})
        return projects

    def add_server(self, project_name, vserver_name):
        c = self.conn.cursor()
        row = c.execute("SELECT id FROM projects WHERE name=?", (project_name,)).fetchone()
        if not row:
            raise ValueError(f"Project '{project_name}' does not exist")
        pid = row[0]
        with self.conn:
            self.conn.execute(
                "INSERT OR IGNORE INTO project_servers (project_id, vserver_name) VALUES (?, ?)",
                (pid, vserver_name),
            )

    def remove_server(self, project_name, vserver_name):
        c = self.conn.cursor()
        row = c.execute("SELECT id FROM projects WHERE name=?", (project_name,)).fetchone()
        if not row:
            raise ValueError(f"Project '{project_name}' does not exist")
        pid = row[0]
        with self.conn:
            self.conn.execute(
                "DELETE FROM project_servers WHERE project_id=? AND vserver_name=?",
                (pid, vserver_name),
            )

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()
