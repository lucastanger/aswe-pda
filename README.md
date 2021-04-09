<p align="center">
  <img width="" height="250" alt="JARVIS Logo" src="https://github.com/lucastanger/aswe-pda/blob/main/docs/readme/jarvis.png">
  <h2 align="center">🤖 Personal Digital Agent</h2>
  <p align="center">Personal Digital Assistant constructed within a Microservice Environment</p>
</p>
<p align="center">
  <a href="https://github.com/lucastanger/aswe-pda/releases">
    <img alt="Release Version" src="https://img.shields.io/github/v/release/lucastanger/aswe-pda">
  </a>
  <a href="https://travis-ci.com/lucastanger/aswe-pda">
    <img alt="Travis (.com)" src="https://travis-ci.com/lucastanger/aswe-pda.svg?token=NpSo3QkoAPuqvyxKepVV&branch=main">
  </a>
  <a href="#">
    <img alt="Codacy Badge" src="https://api.codacy.com/project/badge/Grade/70fc6e8580b84f6fb0f4671b40d0f867">
  </a>
  <a href="https://conventionalcommits.org">
    <img alt="Conventiona Commits" src="https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg">
  </a>
  <a href="https://gitmoji.carloscuesta.me">
    <img alt="Gitmoji" src="https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg?style=flat">
  </a>
</p>

<br>

## Description

Personal Digital Assistant (PDA) named J.A.R.V.I.S. This project emerged from the requirements of a study project. The PDA is build with a Microservice Architecture. This PDA is using Dialogflow, a lifelike conversational AI with state-of-the-art virtual agents.

## Architecture

A microservice approach was used.

<p align="center">
  <img width="" height="" alt="architecture" src="https://github.com/lucastanger/aswe-pda/blob/main/docs/readme/architecture.png">
</p>

## Documentation :memo:

All services have a Postman collection and environment in the docs folder. Also each service is hosting it's own swagger documentation available under the url /rest/api/v1/docs. There you can try out and explore the endpoints.

- [Technical documentation](https://docs.google.com/document/d/1vYbFvzILbU0VHADzpRVWzccZAGCDfMtdo2YaQ_iHPfE/edit?usp=sharing)
- [Requirements documentation](https://docs.google.com/document/d/1GR8EfAHzPDneJrnBjNVnC-X-WyYt78zL4SrSFzMM0ao/edit?usp=sharing)
- [Configuration documentation](https://docs.google.com/spreadsheets/d/1b7tC3VU1Bdlx8nBJZ2YPuD7uMPTM7q6DpHfcT_DpPlI/edit?usp=sharing)
- [Project Organisation](https://docs.google.com/document/d/1FAapj3vPFWIAq8K-GzZUHcewzh18b3yJKtpwSLd8w30/edit?usp=sharing)

## How to use

### Docker :whale:

**Prerequisites:**
- Docker Engine 19.03.0+
- Compose 1.27.0+

```bash
docker-compose up
```

### Local

#### Frontend

Compile Tailwind Stylesheet

![Tailwind GIF](https://github.com/lucastanger/aswe-pda/blob/main/docs/readme/tailwind_install.gif)

#### Backend

**Prerequisites:**
- Python >= 3.8.5

```bash
cd src/backend/services/<service-of-my-choice>
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
python3 app.py # some services use server.py
```

## Built with :hammer_and_wrench:

- [Flask](https://flask.palletsprojects.com) - Python Webframework
- [Docker](https://www.docker.com/) - Container Software
- [tailwindcss](https://tailwindcss.com/) - CSS Framework
- [Node.js](https://nodejs.org/en/) - JavaScript Runtime
- [Pytest](https://docs.pytest.org/en/stable/) - Python testing tool
- [Travis CI](https://travis-ci.org/) - CI
- [Dialogflow](https://cloud.google.com/dialogflow) - Lifelike conversational AI with state-of-the-art virtual agents
- [Postman](https://www.postman.com/) - API Testing
- [Swagger](https://swagger.io/) - API documentation

## Authors :busts_in_silhouette:

-   [**Andrea Budimir**](https://github.com/Merida31) - Requirements Lead - [Student @ DHBW Stuttgart](https://www.dhbw-stuttgart.de/home/)
-   [**Florian Drinkler**](https://github.com/Drinkler) - Developer - [Student @ DHBW Stuttgart](https://www.dhbw-stuttgart.de/home/)
-   [**Hakim Assadi**](https://github.com/HakimAssadi) - Developer - [Student @ DHBW Stuttgart](https://www.dhbw-stuttgart.de/home/)
-   [**Luca Massa**](https://github.com/Haiyn) - Product Owner - [Student @ DHBW Stuttgart](https://www.dhbw-stuttgart.de/home/)
-   [**Luca Stanger**](https://github.com/lucastanger) - Technical Lead, Developer - [Student @ DHBW Stuttgart](https://www.dhbw-stuttgart.de/home/)
-   [**Timo Ströhlein**](https://github.com/TimoStroehlein) - Scrum Master, Developer - [Student @ DHBW Stuttgart](https://www.dhbw-stuttgart.de/home/)

## Copyright :copyright:

Copyright :copyright: 2021 Florian Drinkler, Luca Stanger, Hakim Assadi, Andrea Budimir, Timo Ströhlein, Luca Massa

## License :page_facing_up:
[![GitHub](https://img.shields.io/github/license/lucastanger/aswe-pda)](https://www.github.com/lucastanger/aswe-pda/blob/master/LICENSE)

This project is licensed under the **MIT License** - see the [LICENSE.MD](https://www.github.com/lucastanger/aswe-pda/blob/master/LICENSE) files for details
