# Smile_Detection

![image](https://github.com/user-attachments/assets/eb12b0b0-6b91-48fc-bd54-ac1a49c4030c)

## Smile Detection using Dlib's facial landmarks model

Let's detect the people smiling (smile.mp4) using Dlib's facial landmarks model.

## How it works?

Implementation Logic:

1.Facial Landmark Extraction:
Uses Dlib's 68-point model to identify:

- Mouth corners (points 48 & 54 in 0-index)

- Jaw extremes (points 0 & 16)

2.Distance Calculations:

- Lip Width: Distance between mouth corners

- Jaw Width: Distance between jaw extremes

3.Smile Detection:
Smiling increases lip width relative to jaw width. The threshold of 0.3 was determined through empirical testing on sample videos to optimize detection accuracy.

Key Advantages:

- Normalizes for face size using jaw width

- Real-time performance through simple geometric calculations

- Robust to minor head rotations due to ratio-based approach
