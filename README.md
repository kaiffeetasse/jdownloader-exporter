JDownloader Exporter
====================

A Prometheus exporter for exporting JDownloader metrics. In order to use this exporter, you need to install
the [JDownloader](https://jdownloader.org) client and connect your My.JDownloader account in the settings.

![minecraft-exporter](https://github.com/kaiffeetasse/jdownloader-exporter/raw/master/images/grafana-screenshot.png)

## Metrics

Currently, the following metrics are exported:

* `jdownloader_download_speed` - The current download speed in bytes per second.
* `jdownloader_download_package_count` - The number of packages currently in the download queue.
* `jdownloader_linkgrabber_package_count` - The number of packages currently in the linkgrabber queue.
* `jdownloader_total_bytes_to_download` - The total number of bytes to download.
* `jdownloader_total_bytes_in_linkgrabber` - The total number of bytes in the linkgrabber queue.
* `jdownloader_total_bytes_downloaded` - The total number of bytes downloaded.
* `jdownloader_running_downloads` - The number of running downloads.

#### Prometheus Metrics

```
# HELP jdownloader_download_speed Download Speed in bps
# TYPE jdownloader_download_speed gauge
jdownloader_download_speed{device_name="pils"} 0.0
# HELP jdownloader_download_package_count Download Package Count
# TYPE jdownloader_download_package_count gauge
jdownloader_download_package_count{device_name="pils"} 2.0
# HELP jdownloader_linkgrabber_package_count Linkgrabber Package Count
# TYPE jdownloader_linkgrabber_package_count gauge
jdownloader_linkgrabber_package_count{device_name="pils"} 6.0
# HELP jdownloader_total_bytes_to_download Total Bytes to download
# TYPE jdownloader_total_bytes_to_download gauge
jdownloader_total_bytes_to_download{device_name="pils"} 1.93032336445e+011
# HELP jdownloader_total_bytes_in_linkgrabber Total Bytes in linkgrabber
# TYPE jdownloader_total_bytes_in_linkgrabber gauge
jdownloader_total_bytes_in_linkgrabber{device_name="pils"} 4.79998322106e+011
# HELP jdownloader_total_bytes_downloaded Total Bytes Downloaded
# TYPE jdownloader_total_bytes_downloaded gauge
jdownloader_total_bytes_downloaded{device_name="pils"} 1.3219006063e+010
# HELP jdownloader_running_downloads Running Downloads
# TYPE jdownloader_running_downloads gauge
jdownloader_running_downloads{device_name="pils"} 0.0
```

## Usage

### Configuration

Create a `.env` file with your JDownloader credentials and put it in the root of the project.

Example `.env` file:

```
MYJD_USERNAME="me@example.com"
MYJD_PASSWORD="s3cur3"
EXPORT_INTERVAL_SECONDS=15
```

### Run with Docker Compose

```
docker build --tag jdownloader-exporter:latest .
docker-compose up -d
```

To update the exporter, you can use the `update.sh` script.
