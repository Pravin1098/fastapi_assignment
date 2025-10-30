from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta

app = FastAPI(title="Calendly Mock API", version="1.0")