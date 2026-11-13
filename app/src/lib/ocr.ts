import TextRecognition from "@react-native-ml-kit/text-recognition";
import { linesToMessages, type Message, type OcrLine } from "./transcript";

/**
 * Lit le texte d'une capture d'écran SUR LE TÉLÉPHONE (ML Kit, aucun envoi réseau),
 * puis reconstitue la conversation. Nécessite un build de développement (pas Expo Go).
 */
export async function readConversation(uri: string, imageWidth: number): Promise<Message[]> {
  const result = await TextRecognition.recognize(uri);
  const lines: OcrLine[] = result.blocks.flatMap((b) =>
    b.lines.map((l) => ({ text: l.text, frame: l.frame }))
  );
  return linesToMessages(lines, imageWidth);
}
