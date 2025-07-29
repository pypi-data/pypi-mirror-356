import argparse
from cruxes import Cruxes


def main():
    parser = argparse.ArgumentParser(
        description="Cruxes: Climbing Analysis Toolbox CLI"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Warp subcommand
    warp_parser = subparsers.add_parser(
        "warp", help="Warp a video to match a reference image."
    )
    warp_parser.add_argument("--ref_img", required=True, help="Reference image path.")
    warp_parser.add_argument(
        "--src_video_path", required=True, help="Source video path."
    )
    warp_parser.add_argument(
        "--type", default="dynamic", choices=["dynamic", "fixed"], help="Warp type."
    )

    # Body trajectory subcommand
    body_parser = subparsers.add_parser(
        "body-trajectory", help="Draw body movement trajectories on a video."
    )
    body_parser.add_argument("--video_path", required=True, help="Input video path.")
    body_parser.add_argument(
        "--track_point",
        nargs="*",
        default=["hip_mid", "left_hand", "right_hand"],
        help="Points of interest to track.",
    )
    body_parser.add_argument(
        "--overlay_trajectory", action="store_true", help="Overlay trajectory mask."
    )
    body_parser.add_argument(
        "--draw_pose", action="store_true", help="Draw pose skeleton."
    )
    body_parser.add_argument(
        "--kalman_settings",
        nargs=2,
        metavar=("USE_KALMAN", "KALMAN_GAIN"),
        help="Kalman filter settings: USE_KALMAN(bool) KALMAN_GAIN(float)",
    )
    body_parser.add_argument(
        "--trajectory_png_path", default=None, help="Output PNG path for trajectory."
    )

    args = parser.parse_args()
    cruxes = Cruxes()

    if args.command == "warp":
        cruxes.warp_video(
            args.ref_img,
            args.src_video_path,
            warp_type=args.type,
        )
    elif args.command == "body-trajectory":
        kalman_settings = None
        if args.kalman_settings:
            use_kalman = args.kalman_settings[0].lower() in ("true", "1", "yes")
            kalman_gain = float(args.kalman_settings[1])
            kalman_settings = [use_kalman, kalman_gain]
        cruxes.body_trajectory(
            args.video_path,
            track_point=args.track_point,
            overlay_trajectory=args.overlay_trajectory,
            draw_pose=args.draw_pose,
            kalman_settings=kalman_settings,
            trajectory_png_path=args.trajectory_png_path,
        )


if __name__ == "__main__":
    main()
