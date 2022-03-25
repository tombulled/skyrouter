from . import client
import prometheus_client as prometheus
import fastapi

router = client.SkyRouter(password='...')

registry = prometheus.CollectorRegistry()

transmitted_packets = prometheus.Gauge('transmitted_packets', 'Total number of transmitted packets since last boot', ['port'], registry=registry)
received_packets = prometheus.Gauge('received_packets', 'Total number of received packets since last boot', ['port'], registry=registry)
transmitted_bytes_per_second = prometheus.Gauge('transmitted_bytes_per_second', 'Total number of bytes transmitted per second', ['port'], registry=registry)
received_bytes_per_second = prometheus.Gauge('received_bytes_per_second', 'Total number of bytes received per second', ['port'], registry=registry)
collision_packets = prometheus.Gauge('collision_packets', 'Total number of packet collisions', ['port'], registry=registry)

def update():
    print('updating...')

    statistics = router.system()

    for stats in statistics:
        transmitted_packets.labels(port=stats.port).set(stats.transmitted_packets)
        received_packets.labels(port=stats.port).set(stats.received_packets)
        transmitted_bytes_per_second.labels(port=stats.port).set(stats.transmitted_bytes_per_second)
        received_bytes_per_second.labels(port=stats.port).set(stats.received_bytes_per_second)
        collision_packets.labels(port=stats.port).set(stats.collision_packets)

    print(statistics)

app = fastapi.FastAPI()

@app.get('/', response_class=fastapi.responses.PlainTextResponse)
async def index() -> str:
    print('got request')

    update()

    return prometheus.generate_latest(registry)