from utils.task_worker.task_worker import PlayerTaskWorker


async def send_message_to_task_worker(message: dict | list):
    await PlayerTaskWorker().send_message(message)
