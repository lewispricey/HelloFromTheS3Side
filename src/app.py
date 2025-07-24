from fastapi import FastAPI, HTTPException
import boto3
from os import environ

app = FastAPI()


@app.get("/api/healthcheck")
def health_check():
    return {"status": "online"}

@app.get("/api/songs/{song_name}")
def get_song(song_name: str):
    client = boto3.client('s3')
    bucket_name = environ.get('S3_BUCKET_NAME', '')
    try:
        response = client.get_object(Bucket=bucket_name, Key=f'{song_name}.txt')
        song_data = response['Body'].read()
        return {"song_name": song_name, "lyrics": song_data.decode('utf-8')}
    except client.exceptions.NoSuchKey:
        raise HTTPException(404, {"error": "Song not found"})
    except Exception as e:
        raise HTTPException(500, {"error": str(e)})