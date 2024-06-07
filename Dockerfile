FROM python:3
ARG DISCORD_KEY
ENV DISCORD_API_KEY=$DISCORD_KEY
COPY bot.py .
RUN pip install discord
CMD [ "python", "./bot.py" ]
