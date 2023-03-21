from models._model import TOKENIZER, STANCE_MODEL,DEVICE, StanceDataset
import torch
from torch.utils.data import DataLoader, Dataset

def single_prediction(title:str) -> int:
    title_tokenized = TOKENIZER([title], add_special_tokens = False)
    title_dataset = StanceDataset([title], title_tokenized, [1])
    title_loader = DataLoader(title_dataset, batch_size=16, pin_memory = True)
    STANCE_MODEL.eval()
    with torch.no_grad():
        for batch in title_loader:
            output = STANCE_MODEL(input_ids = batch[0].to(DEVICE), token_type_ids = batch[1].to(DEVICE), attention_mask = batch[2].to(DEVICE))
            predict_label = torch.argmax(output.logits, dim=1)

    return int(predict_label)-1