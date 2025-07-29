
import os
import time
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageGrab


class MediaCapture:
    def __init__(self):
        pass

    def ensureDir(self, path: str) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)

    def captureScreen(self, mediaFile: str) -> str | None:
        """Captures a screenshot and saves it to the given file."""
        try:
            self.ensureDir(mediaFile)
            screenShot = ImageGrab.grab().convert("RGB")
            screenShot.save(mediaFile, quality=15)
            return mediaFile
        except Exception as e:
            print(f"Error occurred while capturing screen: {e}")
            return None

    def recordScreen(self, mediaFile: str, duration: int = 10) -> str | None:
        """Records the screen for a specified duration and saves it to the given file."""
        duration = max(1, min(int(duration), 60))
        screenWidth, screenHeight = ImageGrab.grab().size

        self.ensureDir(mediaFile)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(mediaFile, fourcc, 10.0, (screenWidth, screenHeight))

        frameCount = 0
        maxFrames = int(10 * duration)

        try:
            while frameCount < maxFrames:
                frame = np.array(ImageGrab.grab())
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                out.write(frame)
                frameCount += 1
                time.sleep(1.0 / 10.0)
            return mediaFile
        except Exception as e:
            print(f"Error occurred while recording screen: {e}")
            return None
        finally:
            out.release()
            cv2.destroyAllWindows()

    def captureMedia(self, combinedFile: str, *cameraIndexes: int, normalize: bool = False) -> str | None:
        """Captures images from multiple cameras and combines them into a single image."""
        cameras = []
        try:
            cameras = [cv2.VideoCapture(idx) for idx in cameraIndexes]
            if not all(cam.isOpened() for cam in cameras):
                return None

            time.sleep(2)
            for _ in range(5):
                frames = [cam.read()[1] for cam in cameras]
                if all(frame is not None for frame in frames):
                    break
                time.sleep(0.1)
            else:
                return None

            if normalize:
                frames = [self.normalizeImage(frame) for frame in frames]

            self.ensureDir(combinedFile)
            combinedFrame = np.hstack(frames)
            success = cv2.imwrite(combinedFile, combinedFrame)
            return combinedFile if success else None
        except Exception as e:
            print(f"Error occurred while capturing media: {e}")
            return None
        finally:
            for cam in cameras:
                cam.release()
            cv2.destroyAllWindows()

    def recordMedia(self, combinedFile: str, *cameraIndexes: int, duration: int = 10, normalize: bool = False) -> str | None:
        """Records video from multiple cameras and combines them into a single video file."""
        duration = max(1, min(int(duration), 60))
        cameras = [cv2.VideoCapture(idx) for idx in cameraIndexes]
        if not all(cam.isOpened() for cam in cameras):
            for cam in cameras:
                cam.release()
            return None

        time.sleep(2)
        frameWidth = int(cameras[0].get(cv2.CAP_PROP_FRAME_WIDTH))
        frameHeight = int(cameras[0].get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cameras[0].get(cv2.CAP_PROP_FPS) or 30

        self.ensureDir(combinedFile)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        videoSize = (frameWidth * len(cameras), frameHeight)
        out = cv2.VideoWriter(combinedFile, fourcc, fps, videoSize)

        frameCount = 0
        maxFrames = int(fps * duration)

        try:
            while frameCount < maxFrames:
                frames = []
                for idx, cam in enumerate(cameras):
                    ret, frame = cam.read()
                    if not ret:
                        print(f"Error: Frame capture failed for camera {cameraIndexes[idx]}")
                        return None
                    if normalize:
                        frame = self.normalizeImage(frame)
                    label = f"View {idx+1}"
                    cv2.putText(frame, label, (10, frameHeight - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                    frames.append(frame)
                combinedFrame = np.hstack(frames)
                out.write(combinedFrame)
                frameCount += 1
            return combinedFile
        except Exception as e:
            print(f"Error occurred while recording: {e}")
            return None
        finally:
            for cam in cameras:
                cam.release()
            out.release()
            cv2.destroyAllWindows()

    def streamScreen(self, fps: int = 10, maxWidth: int = 1280, maxHeight: int = 720):
        """Yields live, resized screen frames as numpy arrays at the given FPS."""
        interval = 1.0 / fps
        try:
            while True:
                frame = np.array(ImageGrab.grab())
                h, w = frame.shape[:2]
                scale = min(maxWidth / w, maxHeight / h, 1.0)
                if scale < 1.0:
                    frame = cv2.resize(frame, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
                yield frame
                time.sleep(interval)
        except KeyboardInterrupt:
            return

    def streamCameras(self, *cameraIndexes: int, normalize: bool = False, fps: int = 30,
                      maxWidth: int = 1280, maxHeight: int = 720):
        """Yields live, resized frames from the given cameras as (frame list, frame count)."""
        cameras = [cv2.VideoCapture(idx) for idx in cameraIndexes]
        try:
            if not all(cam.isOpened() for cam in cameras):
                yield None
                return
            frameCount = 0
            while True:
                frames = []
                for cam in cameras:
                    ret, frame = cam.read()
                    if not ret:
                        frames.append(None)
                    else:
                        if normalize:
                            frame = self.normalizeImage(frame)
                        h, w = frame.shape[:2]
                        scale = min(maxWidth / w, maxHeight / h, 1.0)
                        if scale < 1.0:
                            frame = cv2.resize(frame, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
                        frames.append(frame)
                yield frames, frameCount
                frameCount += 1
                time.sleep(1.0 / fps)
        except KeyboardInterrupt:
            return
        finally:
            for cam in cameras:
                cam.release()
            cv2.destroyAllWindows()

    def normalizeImage(self, image: np.ndarray) -> np.ndarray:
        """Applies CLAHE and gamma correction to normalize the image."""
        lab     = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe   = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l       = clahe.apply(l)
        lab     = cv2.merge((l, a, b))
        image   = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

        gray           = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        meanBrightness = np.mean(gray)
        gamma          = 1.3 if meanBrightness < 80 else 1.1 if meanBrightness < 130 else 1.0

        invGamma = 1.0 / gamma
        table    = np.array([(i / 255.0) ** invGamma * 255 for i in range(256)]).astype("uint8")

        return cv2.LUT(image, table)


# Example usage of the MediaCapture class
#mediaCapture = MediaCapture()

# # Stream screen preview in real time
# for frame in mediaCapture.streamScreen(fps=15):
#     # Show the frame (with cv2, PIL, etc.) or process it
#     cv2.imshow("Screen", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# cv2.destroyAllWindows()

# # Stream from cameras
# for frames, frameCount in mediaCapture.streamCameras(0, 1, normalize=True):
#     if any(f is None for f in frames):
#         break
#     combined = np.hstack(frames)
#     cv2.imshow("Combined Cameras", combined)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# cv2.destroyAllWindows()
