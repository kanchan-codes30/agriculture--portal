import sys
import joblib

model = joblib.load("crop_model.pkl")

N = float(sys.argv[1])
P = float(sys.argv[2])
K = float(sys.argv[3])
temp = float(sys.argv[4])
humidity = float(sys.argv[5])
ph = float(sys.argv[6])
rainfall = float(sys.argv[7])

prediction = model.predict([[N,P,K,temp,humidity,ph,rainfall]])

print(prediction[0])