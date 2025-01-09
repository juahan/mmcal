# MMcal

Takes inspiration from the Magic Mirror calendar and loosely converts it to a custom integration for Home Assistant that allows you to display calendar events from an iCalendar URL.

## Installation

1. Clone this repository into your Home Assistant `custom_components` directory:

    ```sh
    git clone https://github.com/juahan/magic_mirror_calendar.git custom_components/mmcal
    ```

## Configuration

1. Add the following to your `configuration.yaml`:

    ```yaml
    magic_mirror_calendar:
      url: "YOUR_ICALENDAR_URL"
      max_events: 20
      calendar_name: "Calendar name"
    ```

2. Restart Home Assistant.

## Usage

After installation and configuration, the Magic Mirror Calendar integration will fetch events from the specified iCalendar URL and display them on your Magic Mirror.

## Files

- __init__.py: Initializes the integration and sets up the data update coordinator.
- calendar.py: Defines the calendar platform and entities.
- config_flow.py: Handles the configuration flow for setting up the integration.
- const.py: Contains constants used throughout the integration.
- manifest.json: Metadata about the integration.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## Support

For any issues or questions, please open an issue on the [GitHub repository](https://github.com/juahan/magic_mirror_calendar).
