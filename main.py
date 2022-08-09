import logging
import os
import time
from dotenv import load_dotenv
from prometheus_client import Gauge, start_http_server
import myjd_api.myjdapi as myjd_api

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

MYJD_USERNAME = os.environ.get("MYJD_USERNAME")
MYJD_PASSWORD = os.environ.get("MYJD_PASSWORD")
EXPORT_INTERVAL_SECONDS = int(os.environ.get("EXPORT_INTERVAL_SECONDS"))


def export_metrics():
    download_speed_gauge = Gauge(
        "jdownloader_download_speed",
        "Download Speed in bps",
        ["device_name"]
    )

    download_package_count_gauge = Gauge(
        "jdownloader_download_package_count",
        "Download Package Count",
        ["device_name"]
    )

    linkgrabber_package_count_gauge = Gauge(
        "jdownloader_linkgrabber_package_count",
        "Linkgrabber Package Count",
        ["device_name"]
    )

    total_bytes_to_download_gauge = Gauge(
        "jdownloader_total_bytes_to_download",
        "Total Bytes to download",
        ["device_name"]
    )

    total_bytes_in_linkgrabber_gauge = Gauge(
        "jdownloader_total_bytes_in_linkgrabber",
        "Total Bytes in linkgrabber",
        ["device_name"]
    )

    total_bytes_downloaded_gauge = Gauge(
        "jdownloader_total_bytes_downloaded",
        "Total Bytes Downloaded",
        ["device_name"]
    )

    running_downloads_gauge = Gauge(
        "jdownloader_running_downloads",
        "Running Downloads",
        ["device_name"]
    )

    start_http_server(8008)

    while True:
        try:

            jd = myjd_api.Myjdapi()

            jd.connect(MYJD_USERNAME, MYJD_PASSWORD)

            jd.update_devices()
            jd_devices = jd.list_devices()
            logger.debug("available jd devices for " + str(MYJD_USERNAME) + ": " + str(jd_devices))

            if len(jd_devices) == 0:
                logger.info("0 devices available")
                return False
            else:

                for jd_device in jd_devices:
                    logger.info("exporting metrics for " + str(jd_device['name']))

                    device = jd.get_device(device_id=jd_device['id'])
                    device.disable_direct_connection()

                    download_packages = device.downloads.query_packages()
                    download_links = device.downloads.query_links()
                    linkgrabber_packages = device.linkgrabber.query_packages()

                    # current download speed
                    download_speed = device.downloadcontroller.get_speed_in_bytes()
                    logger.info("download speed: " + str(download_speed) + " bps")
                    download_speed_gauge.labels(device.name).set(download_speed)

                    # downloads package count
                    download_package_count = len(download_packages)
                    logger.info("download package count: " + str(download_package_count))
                    download_package_count_gauge.labels(device.name).set(download_package_count)

                    # linkgrabber package count
                    linkgrabber_package_count = device.linkgrabber.get_package_count()
                    logger.info("linkgrabber package count: " + str(linkgrabber_package_count))
                    linkgrabber_package_count_gauge.labels(device.name).set(linkgrabber_package_count)

                    # total bytes in downloads
                    total_bytes_to_download = 0
                    for download_package in download_packages:
                        total_bytes_to_download += download_package['bytesTotal']
                    logger.info("total bytes to download: " + str(total_bytes_to_download))
                    total_bytes_to_download_gauge.labels(device.name).set(total_bytes_to_download)

                    # total bytes in linkgrabber
                    total_bytes_to_download_linkgrabber = 0
                    for linkgrabber_package in linkgrabber_packages:
                        total_bytes_to_download_linkgrabber += linkgrabber_package['bytesTotal']
                    logger.info("total bytes in linkgrabber: " + str(total_bytes_to_download_linkgrabber))
                    total_bytes_in_linkgrabber_gauge.labels(device.name).set(total_bytes_to_download_linkgrabber)

                    # total bytes downloaded
                    total_bytes_downloaded = 0
                    for download_package in download_packages:
                        total_bytes_downloaded += download_package['bytesLoaded']
                    logger.info("total bytes downloaded: " + str(total_bytes_downloaded))
                    total_bytes_downloaded_gauge.labels(device.name).set(total_bytes_downloaded)

                    # running downloads
                    running_downloads = 0
                    for download_link in download_links:

                        if 'running' in download_link:
                            if download_link['running']:
                                running_downloads += 1

                    logger.info("running downloads: " + str(running_downloads))
                    running_downloads_gauge.labels(device.name).set(running_downloads)

        except Exception as e:
            logger.error("Error while getting server stats:")
            logger.exception(e)

        time.sleep(EXPORT_INTERVAL_SECONDS)


if __name__ == '__main__':
    export_metrics()
