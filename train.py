import json
from random import shuffle
from nltk import * 
from nltk_uitls import bag_of_word, tokenize, stem
import numpy as np
# from lib2to3.pgen2.tokenize import tokenize

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from model import NeuralNet

with open('intent.json','r') as f:
   intents = json.load(f) 

all_words=[]
tags= []
xy = []
for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        # print(pattern)
        w = tokenize(pattern)
        all_words.extend(w)
        xy.append((w, tag))

ignore_words = ['?','!','.',',']
all_words = [stem(w) for w in all_words if w not in ignore_words]
all_words = sorted(set(all_words))
tags = sorted(set(tags))
# print(tags)

x_train = []
y_train = []
for (pattern_sentence, tag) in xy:
    bag = bag_of_word(pattern_sentence, all_words)
    x_train.append(bag)

    label = tags.index(tag)
    y_train.append(label) # CrossEntropyloss
x_train = np.array(x_train)
y_train = np.array(y_train)
print("x_train", x_train)
print("y_train", y_train)

batch_size = 8
hidden_size = 8
output_size = len(tags)
input_size = len(x_train[0])
learning_rate = 0.001
num_epochs = 1000

class ChatDataset(Dataset):
    def __init__(self):
        self.n_samples = len(x_train)
        self.x_data = x_train
        self.y_data = y_train
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.n_samples
    


# print(input_size, len(all_words))
# print(output_size, tags)

dataset = ChatDataset()
train_loader = DataLoader(dataset= dataset, 
                            batch_size= batch_size, 
                            shuffle=True, 
                            num_workers = 0)

device = torch.device('cuda' if torch.cuda.is_available()  else 'cpu')
print('Which Device is using: ', device)
model = NeuralNet(input_size, hidden_size, output_size).to(device)

#Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
    for (words, labels ) in train_loader:
        words = words.to(device)
        labels = labels.to(dtype=torch.long).to(device)

        #forward pass
        outputs =model(words)
        loss = criterion(outputs, labels)

        #backwards and optimizer step
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    if (epoch +1)% 100 ==0:
        print(f'Epoch [{epoch +1}/{num_epochs}], loss : {loss.item():.4f}')

print(f'final loss:{loss.item():.4f}')


data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "hidden_size": hidden_size,
    "output_size": output_size,
    "all_words": all_words,
    "tags": tags
}
FILE = "data.pth"
torch.save(data,FILE)
print(f'training complete. file saved to {FILE}')