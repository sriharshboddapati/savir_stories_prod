from fastapi import FastAPI


app = FastAPI()


#get function to pull one timeline image from the datastore based on date
@app.get("/")
def get_image():
    return ("Testing")

    