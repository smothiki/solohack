from face2face import Face2Face
import cv2
from media_toolkit import VideoFile
from vidgear.gears import WriteGear


f2f = Face2Face(device_id=0)

def test_single_face_swap():
    source_img = "test/test_media/test_face_1.jpg"
    target_img = "test/test_media/test_face_2.jpg"
    swapped = f2f.swap_img_to_img(source_img, target_img, enhance_face_model=None)
    cv2.imwrite("test_swap.png", swapped)

def test_video_face_swap():
    # output_params = {
    #     "-vcodec": "libx264",  # Correct encoder for H.264
    #     "-acodec": "aac",  # Optional: specify audio codec
    # }
    # writer = WriteGear(output_filename="output.mp4", compression_mode=True, logging=True, **output_params)
    # writer.close()

    # # add ref face
    source_img = cv2.imread("test/test_media/test_face_4.jpg")
    f2f.add_face("caprio", source_img, save=True)
    # swap it
    vf = VideoFile().from_file("test/test_media/test_video_1.mp4")
    # vf = VideoFile().from_file("test/test_media/output.mp4")
    # swapped = f2f.swap_to_face_in_video(face_name="caprio", video=vf)
    swapped = f2f.swap(media=vf, faces="caprio")
    swapped.save("test/test_media/test_video_2_swapped_swapped_smithy.mp4")

if __name__ == "__main__":
    # test_single_face_swap()
    # test_multi_face_swap()
    # test_multi_face_from_reference()
    # test_face_enhancing()
    # test_face_enhancing_single_face()
    # test_multi_face_video_swap()
    test_video_face_swap()
    a = 1