FROM python:3
ARG DISCORD_KEY
ENV DISCORD_API_KEY=$DISCORD_KEY
COPY . .
RUN pip install discord
RUN pip install ffmpeg
CMD [ "python", "./bot.py" ]
