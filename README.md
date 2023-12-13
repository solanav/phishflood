# 1. PhishFlood

PhishFlood is a Python tool that utilizes the Playwright library to automate the process of filling phishing websites with fake credentials. This project is designed for educational and research purposes only. Please use it responsibly and ethically.

## 1.1. Table of content
- [1. PhishFlood](#1-phishflood)
  - [1.1. Table of content](#11-table-of-content)
  - [1.2. Installation](#12-installation)
    - [1.2.1. Prerequisites](#121-prerequisites)
    - [1.2.2. Clone the Repository](#122-clone-the-repository)
    - [1.2.3. Install Dependencies with Poetry](#123-install-dependencies-with-poetry)
  - [1.3. Usage](#13-usage)
    - [1.3.1. Run PhishFlood](#131-run-phishflood)
  - [1.4. Testing](#14-testing)
  - [1.5. Disclaimer](#15-disclaimer)
  - [1.6. Contributing](#16-contributing)
  - [1.7. License](#17-license)


## 1.2. Installation

### 1.2.1. Prerequisites

- Python 3.11 or higher
- Git
- Poetry

### 1.2.2. Clone the Repository

```bash
git clone https://github.com/solanav/phishflood.git
cd phishflood
```

### 1.2.3. Install Dependencies with Poetry

```bash
poetry install
```

## 1.3. Usage

### 1.3.1. Run PhishFlood

```bash
poetry run python -m phishflood --url example.org
```

PhishFlood will launch a Playwright browser instance in the background and start filling in fake credentials on known phishing websites. Make sure to use this tool only in a controlled environment and for educational purposes.

## 1.4. Testing

We use [pytest](https://docs.pytest.org/en/stable/) for testing. To run the tests, use the following command:

```bash
poetry run pytest
```

Make sure to have a controlled testing environment, as the tests involve interactions with websites.

## 1.5. Disclaimer

This tool is meant for educational and research purposes only. Unauthorized use of this tool is strictly prohibited. The developers are not responsible for any misuse or damage caused by this tool.

## 1.6. Contributing

If you would like to contribute to this project, please open an issue or submit a pull request. We welcome any suggestions, improvements, or bug fixes.

## 1.7. License

This project is licensed under the [AGPL License](LICENSE).
