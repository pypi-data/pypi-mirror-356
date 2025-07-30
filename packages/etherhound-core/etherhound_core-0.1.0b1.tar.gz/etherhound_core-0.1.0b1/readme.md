<a id="readme-top"></a>

[![Forks][forks-shield]][forks-url] [![Issues][issues-shield]][issues-url]
[![Contributors][contributors-shield]][contributors-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/EtherHounds/Core">
    <img src="images/ethereum.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">EtherHound (Core)</h3>

  <p align="center">
    The core of EtherHound — fast, flexible Ethereum blockchain event tracker.
    <br />
    <!--<a href="https://github.com/EtherHounds/Core"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/EtherHounds/Core">View Demo</a>
    &middot;
    <a href="https://github.com/EtherHounds/Core/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/EtherHounds/Core/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>-->
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

EtherHound Core is the foundational service of the EtherHound suite — a modular, event-driven blockchain scanner designed to monitor Ethereum networks with high precision.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Web3.py]][Web3-url]
* [![FastAPI]][FastAPI-url]
* [![Pydantic]][Pydantic-url]
* [![Typer]][Typer-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* python >= 3.10
* web3 >= 7.12.0
* fastapi[standard]
* pydantic
* typer (CLI)

### Installation

#### Github installation (recommended):
  1. clone the repo
  ```bash
  git clone https://github.com/EtherHounds/Core.git
  ```
  2. cd into the repo
  ```bash
  cd Core
  ```

  3. build
  ```bash
  pip install . -U
  ```

  4. done!

#### PyPi:
  ```bash
  pip install etherhound-core
  ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

### CLI (hound)

#### deploy 
used to deploy the Hound Server

Args:
  * host (str): the uvicorn server host, default=localhost
  * port (int): the uvicorn server port, default=8080
  * rpc (str): the RPC url from your provider
  * mode (str): the scanner mode, default="fast"
  * detach (bool): de-attach from the server, default=False
  * load_env (bool): get the rpc,mode from the .env file, default=False

<!--_For more examples, please refer to the [Documentation](https://example.com)_-->

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Examples
- [ ] Better Documentation
- [ ] Docker image (docker hub)
- [ ] BlockScanner Implementation

See the [open issues](https://github.com/EtherHounds/Core/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/EtherHounds/Core/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=EtherHounds/Core" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## License

Distributed under the project_license. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

SpicyPenguin - [@kerolis55463](https://t.me/kerolis55463)

Project Link: [https://github.com/EtherHounds/Core](https://github.com/EtherHounds/Core)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>-->



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/EtherHounds/Core.svg?style=for-the-badge
[contributors-url]: https://github.com/EtherHounds/Core/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/EtherHounds/Core.svg?style=for-the-badge
[forks-url]: https://github.com/EtherHounds/Core/network/members
[stars-shield]: https://img.shields.io/github/stars/EtherHounds/Core.svg?style=for-the-badge
[stars-url]: https://github.com/EtherHounds/Core/stargazers
[issues-shield]: https://img.shields.io/github/issues/EtherHounds/Core.svg?style=for-the-badge
[issues-url]: https://github.com/EtherHounds/Core/issues
[license-shield]: https://img.shields.io/github/license/EtherHounds/Core.svg?style=for-the-badge
[license-url]: https://github.com/EtherHounds/Core/blob/master/LICENSE.txt
[Web3.py]: https://img.shields.io/badge/web3.py-%236f7dca?style=for-the-badge&logo=ethers
[Web3-url]: https://web3py.readthedocs.io/en/stable/index.html
[FastAPI]: https://img.shields.io/badge/FastAPI-black?style=for-the-badge&logo=fastapi
[FastAPI-url]: https://fastapi.tiangolo.com/
[Pydantic]: https://img.shields.io/badge/pydantic-darkred?style=for-the-badge&logo=pydantic
[Pydantic-url]: https://docs.pydantic.dev/latest/
[Typer]: https://img.shields.io/badge/typer-black?style=for-the-badge&logo=typer
[Typer-url]: https://typer.tiangolo.com/