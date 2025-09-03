<!--
 Copyright (c) 2025 Innodisk Corp.
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

# iQS-VLM SDK

> If you haven't tried our iqs-vlm application yet, we recommend visiting this [page](../../applications/iqs-vlm/README.md) first, then returning here for customization options and other advanced features.

# User prompt customization

```bash
iqs-launcher --autotag iqs-vlm-demo
```

After running the command, create a file named `iqs_vlm_prompt.txt` in your
current working directory. Edit this file with any text editor to see the VLM
response update dynamically as you make changes.

# Chat with LLaVA-1.5-7B

Alongside the live video demo, you can also chat with **LLaVA-1.5-7B** using
[Open WebUI](https://github.com/open-webui/open-webui).

https://github.com/user-attachments/assets/fda1d4a4-2ef7-40ff-910b-47d563fc3273

1. Start a Open WebUI server on the platform.

   ```bash
   docker run --rm -d -p 3000:8080 \
       -e WEBUI_AUTH=False \
       -e OLLAMA_BASE_URL=http://host.docker.internal:22434 \
       -v open-webui:/app/backend/data \
       --add-host host.docker.internal:host-gateway \
       --name open-webui \
       ghcr.io/open-webui/open-webui:git-b5f4c85
   ```

2. Open `192.168.3.206:3000` using your browser on your development machine.

3. We recommend the following system prompt.

   ```
   A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the human's questions.
   ```

4. Start chatting!

# Technical Details

1. For more details on running LLaVA-1.5-7B on the Qualcomm platform, refer to
   the tutorial available in the Qualcomm Package Manager by searching for
   "Tutorial for LLaVA1.5-7B".

   - Qualcomm Package Manager:
   https://qpm.qualcomm.com/#/main/tools/details/QPM3

2. `OGenie` is an Ollama-compatible API server built with `libGenie`, designed
   to enable LLM/VLM inference on Qualcomm platforms. It implements a subset of
   the Ollama API—specifically `POST /api/chat` and `GET /api/tags`—and currently
   supports only streaming mode. The only available model is
   `llava2_7B_FT:latest`.

   For more details about the API, visit the official Ollama documentation:
   https://ollama.readthedocs.io/en/api/
