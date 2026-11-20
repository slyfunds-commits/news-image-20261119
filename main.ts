import { copyFile, mkdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const repositoryDirectory = path.dirname(fileURLToPath(import.meta.url));

function outputDirectory() {
  if (process.env.MAKEFUN_OUTPUT_DIR) {
    return process.env.MAKEFUN_OUTPUT_DIR;
  }

  const index = process.argv.indexOf("--output");
  if (index !== -1 && process.argv[index + 1]) {
    return process.argv[index + 1];
  }

  const inline = process.argv.find((argument) => argument.startsWith("--output="));
  if (inline) {
    return inline.slice("--output=".length);
  }

  return "/output";
}

async function main() {
  const source = path.join(repositoryDirectory, "entry.png");
  const destinationDirectory = outputDirectory();

  await mkdir(destinationDirectory, { recursive: true });
  try {
    await copyFile(source, path.join(destinationDirectory, "entry.png"));
  } catch (error) {
    if (error.code === "ENOENT" && error.path === source) {
      throw new Error(`Required image is missing: ${source}`, { cause: error });
    }
    throw error;
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
