import { createCanvas } from "@napi-rs/canvas";

// Adapt the browser canvas API to a real PNG renderer for image and DOM tests.
export function imageCanvas() {
  const canvas = createCanvas(1, 1);
  canvas.toBlob = (callback) => {
    canvas.encode("png").then(
      (bytes) => callback(new Blob([bytes], { type: "image/png" })),
      () => callback(null),
    );
  };
  return canvas;
}
