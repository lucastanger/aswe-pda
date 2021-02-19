#!/bin/bash
docker run -d -p 5555:5555 --name t2s-s2t-container --env-file ./ibm-credentials-t2s.env --env-file ./ibm-credentials-s2t.env t2s-s2t-service:1.0
