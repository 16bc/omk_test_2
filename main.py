import uvicorn, cv2
from vidgear.gears.asyncio import WebGear_RTC


class Custom_Stream_Class:

    def __init__(self, source, tl):
        self.source = cv2.VideoCapture(source)
        self.running = True
        self.tl = tl

    def read(self):
        if self.source is None:
            return None
        if self.running:
            (grabbed, frame) = self.source.read()
            if grabbed:
                frame = cv2.resize(frame, (1280, 800))
                # Определяем цвет светофора
                traficLight_frame = frame[self.tl[0]:self.tl[1], self.tl[2]:self.tl[3]]
                traficLight = cv2.resize(traficLight_frame, (1, 1))
                traficLight_value = 'Красный' if traficLight[0, 0][2] > 150 else 'Зеленый'
                cv2.rectangle(frame, (90, 40), (420, 120),
                              (0, 0, 0), -1)
                cv2.putText(frame, traficLight_value, (100, 100), cv2.FONT_HERSHEY_COMPLEX, 2,
                            (255, 255, 255))
                return frame
            else:
                self.running = False
        return None

    def stop(self):
        self.running = False
        if not self.source is None:
            self.source.release()

VIDEO_URL = "https://cams.is74.ru/live/main/cam19385.m3u8"
TL = [520, 529, 634, 641]
options = {
    "custom_data_location": "./",
    "custom_stream": Custom_Stream_Class(source=VIDEO_URL, tl=TL),
    "enable_live_broadcast": True,
    }
web = WebGear_RTC(logging=True, **options)

if __name__ == "__main__":
    uvicorn.run(web(), host="localhost", port=8092)
    # web.shutdown()
