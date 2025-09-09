from core.app import GameApp
from algorithms import bfs_rooks

if __name__ == "__main__":
    solutions = bfs_rooks(8)  # lấy tất cả nghiệm 8 xe
    app = GameApp(solutions)
    app.run()
