import pygame
from collections import deque
import heapq

def reconstruct_path(current, draw_func):
    path_len = 0
    while current.previous:
        path_len += 1
        current = current.previous
        if not current.is_start():
            current.make_path()
            draw_func()
            pygame.time.delay(10)
    return path_len

def bfs(draw_func, start, end, delay_ms):
    queue = deque([start])
    visited = {start}

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False, len(visited), 0

        current = queue.popleft()

        if current == end:
            path_len = reconstruct_path(end, draw_func)
            end.make_end()
            start.make_start()
            draw_func()
            return True, len(visited), path_len

        for neighbor in current.neighbors:
            if neighbor not in visited:
                neighbor.previous = current
                visited.add(neighbor)
                queue.append(neighbor)
                if not neighbor.is_end():
                    neighbor.make_visited()

        draw_func()
        pygame.time.delay(delay_ms)

    return False, len(visited), 0

def dfs(draw_func, start, end, delay_ms):
    stack = [start]
    visited = {start}

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False, len(visited), 0

        current = stack.pop()

        if current == end:
            path_len = reconstruct_path(end, draw_func)
            end.make_end()
            start.make_start()
            draw_func()
            return True, len(visited), path_len

        for neighbor in current.neighbors:
            if neighbor not in visited:
                neighbor.previous = current
                visited.add(neighbor)
                stack.append(neighbor)
                if not neighbor.is_end():
                    neighbor.make_visited()

        draw_func()
        pygame.time.delay(delay_ms)

    return False, len(visited), 0

def dijkstra(draw_func, start, end, delay_ms):
    count = 0
    pq = [(0, count, start)]
    start.distance = 0
    visited = set()

    while pq:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False, len(visited), 0

        current_dist, _, current = heapq.heappop(pq)
        
        if current in visited:
            continue
            
        visited.add(current)

        if current == end:
            path_len = reconstruct_path(end, draw_func)
            end.make_end()
            start.make_start()
            draw_func()
            return True, len(visited), path_len

        for neighbor in current.neighbors:
            temp_dist = current.distance + 1
            
            if temp_dist < neighbor.distance:
                neighbor.previous = current
                neighbor.distance = temp_dist
                count += 1
                heapq.heappush(pq, (temp_dist, count, neighbor))
                if not neighbor.is_end() and neighbor not in visited:
                    neighbor.make_visited()

        draw_func()
        pygame.time.delay(delay_ms)

    return False, len(visited), 0
