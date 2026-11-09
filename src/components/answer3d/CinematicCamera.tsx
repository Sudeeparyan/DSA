"use client";

import { useRef } from "react";
import { useFrame, useThree } from "@react-three/fiber";
import type { CinemaShot } from "@/lib/cinemaCameras";
import { poseForShot } from "@/lib/cinemaCameras";
import * as THREE from "three";

export function CinematicCamera({
  shot,
  progress,
  focus,
  interactive,
}: {
  shot: CinemaShot;
  progress: number;
  focus: [number, number, number];
  interactive?: boolean;
}) {
  const { camera } = useThree();
  const look = useRef(new THREE.Vector3(...focus));

  useFrame(() => {
    if (interactive) return;
    const pose = poseForShot(shot, progress, focus);
    camera.position.lerp(
      new THREE.Vector3(...pose.position),
      0.08,
    );
    look.current.lerp(new THREE.Vector3(...pose.lookAt), 0.1);
    camera.lookAt(look.current);
    if ("fov" in camera) {
      const persp = camera as THREE.PerspectiveCamera;
      persp.fov += (pose.fov - persp.fov) * 0.08;
      persp.updateProjectionMatrix();
    }
  });

  return null;
}
