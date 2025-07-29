import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from src.ipwt_pi.pi_monitor import PIMonitor
import os
import matplotlib.pyplot as plt

class AddGaussianNoise(object):
    def __init__(self, mean=0., std=1.):
        self.std = std
        self.mean = mean
        
    def __call__(self, tensor):
        return tensor + torch.randn(tensor.size()) * self.std + self.mean
    
    def __repr__(self):
        return self.__class__.__name__ + '(mean={0}, std={1})'.format(self.mean, self.std)

class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(2)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(2)
        self.fc1 = nn.Linear(32 * 7 * 7, 64)
        self.relu3 = nn.ReLU()
        self.fc2 = nn.Linear(64, 10)

    def forward(self, x):
        x = self.pool1(self.relu1(self.conv1(x)))
        x = self.pool2(self.relu2(self.conv2(x)))
        x = x.view(-1, 32 * 7 * 7)
        x = self.relu3(self.fc1(x))
        return self.fc2(x)

def train(model, device, train_loader, optimizer, epoch, loss_fn, pi_monitor):
    model.train()
    total_loss = 0
    correct = 0
    all_pi_scores = []
    all_surprises = []
    all_taus = []
    all_taus = []

    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        logits = model(data)
        loss_epsilon = loss_fn(logits, target)
        loss_epsilon.backward()
        optimizer.step()

        pi_metrics = pi_monitor.calculate(model, loss_epsilon, logits)
        all_pi_scores.append(pi_metrics['pi_score'])
        all_surprises.append(pi_metrics['surprise'])
        all_taus.append(pi_metrics['tau'])

        total_loss += loss_epsilon.item()
        pred = logits.argmax(dim=1, keepdim=True)
        correct += pred.eq(target.view_as(pred)).sum().item()

        if batch_idx % 100 == 0:
            print(f"Train Epoch: {epoch} [{batch_idx * len(data)}/{len(train_loader.dataset)} ({100. * batch_idx / len(train_loader):.0f}%)]\tLoss: {loss_epsilon.item():.6f}\tPI: {pi_metrics['pi_score']:.4f}\tSurprise: {pi_metrics['surprise']:.4f}\tTau: {pi_metrics['tau']:.4f}")
    
    avg_loss = total_loss / len(train_loader)
    accuracy = 100. * correct / len(train_loader.dataset)
    avg_pi_score = sum(all_pi_scores) / len(all_pi_scores) if all_pi_scores else 0
    avg_surprise = sum(all_surprises) / len(all_surprises) if all_surprises else 0
    avg_tau = sum(all_taus) / len(all_taus) if all_taus else 0

    print(f"Train set: Average loss: {avg_loss:.4f}, Accuracy: {correct}/{len(train_loader.dataset)} ({accuracy:.0f}%)\tAvg PI: {avg_pi_score:.4f}\tAvg Surprise: {avg_surprise:.4f}\tAvg Tau: {avg_tau:.4f}")
    return avg_loss, accuracy, avg_pi_score, avg_surprise, avg_tau

def validate(model, device, val_loader, loss_fn, pi_monitor, dataset_name="Validation"):
    model.eval()
    val_loss = 0
    correct = 0
    
    all_pi_scores = []
    all_surprises = []
    all_taus = []

    for data, target in val_loader:
        data, target = data.to(device), target.to(device)
        
        logits = model(data)
        loss_epsilon = loss_fn(logits, target)
        
        model.zero_grad()
        loss_epsilon.backward()
        
        pi_metrics = pi_monitor.calculate(model, loss_epsilon, logits)
        all_pi_scores.append(pi_metrics['pi_score'])
        all_surprises.append(pi_metrics['surprise'])
        all_taus.append(pi_metrics['tau'])

        with torch.no_grad():
            val_loss += loss_epsilon.item()
            pred = logits.argmax(dim=1, keepdim=True)
            correct += pred.eq(target.view_as(pred)).sum().item()

    avg_val_loss = val_loss / len(val_loader)
    accuracy = 100. * correct / len(val_loader.dataset)
    
    avg_pi_score = sum(all_pi_scores) / len(all_pi_scores) if all_pi_scores else 0
    avg_surprise = sum(all_surprises) / len(all_surprises) if all_surprises else 0
    avg_tau = sum(all_taus) / len(all_taus) if all_taus else 0

    print(f"{dataset_name} set: Average loss: {avg_val_loss:.4f}, Accuracy: {correct}/{len(val_loader.dataset)} ({accuracy:.0f}%)\tAvg PI: {avg_pi_score:.4f}\tAvg Surprise: {avg_surprise:.4f}\tAvg Tau: {avg_tau:.4f}")
    return avg_val_loss, accuracy, avg_pi_score, avg_surprise, avg_tau

def plot_metrics(metrics, output_dir):
    epochs = range(1, len(metrics['train_loss']) + 1)

    plt.figure(figsize=(18, 15)) # Adjusted for 5 plots

    # Plot Loss
    plt.subplot(3, 2, 1)
    plt.plot(epochs, metrics['train_loss'], label='Train Loss')
    plt.plot(epochs, metrics['val_loss'], label='MNIST Val Loss')
    plt.plot(epochs, metrics['ood_val_loss'], label='FashionMNIST OOD Val Loss')
    plt.plot(epochs, metrics['noisy_val_loss'], label='Noisy MNIST Val Loss')
    plt.title('Loss over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()

    # Plot Accuracy
    plt.subplot(3, 2, 2)
    plt.plot(epochs, metrics['train_acc'], label='Train Accuracy')
    plt.plot(epochs, metrics['val_acc'], label='MNIST Val Accuracy')
    plt.plot(epochs, metrics['ood_val_acc'], label='FashionMNIST OOD Val Accuracy')
    plt.plot(epochs, metrics['noisy_val_acc'], label='Noisy MNIST Val Accuracy')
    plt.title('Accuracy over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy (%)')
    plt.legend()

    # Plot PI
    plt.subplot(3, 2, 3)
    plt.plot(epochs, metrics['train_pi'], label='Train PI')
    plt.plot(epochs, metrics['val_pi'], label='MNIST Val PI')
    plt.plot(epochs, metrics['ood_val_pi'], label='FashionMNIST OOD Val PI')
    plt.plot(epochs, metrics['noisy_val_pi'], label='Noisy MNIST Val PI')
    plt.title('Predictive Integrity (PI) over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('PI Score')
    plt.legend()

    # Plot Surprise
    plt.subplot(3, 2, 4)
    plt.plot(epochs, metrics['train_surprise'], label='Train Surprise')
    plt.plot(epochs, metrics['val_surprise'], label='MNIST Val Surprise')
    plt.plot(epochs, metrics['ood_val_surprise'], label='FashionMNIST OOD Val Surprise')
    plt.plot(epochs, metrics['noisy_val_surprise'], label='Noisy MNIST Val Surprise')
    plt.title('Surprise (Gradient Norm) over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('Surprise')
    plt.legend()

    # Plot Tau
    plt.subplot(3, 2, 5)
    plt.plot(epochs, metrics['train_tau'], label='Train Tau')
    plt.plot(epochs, metrics['val_tau'], label='MNIST Val Tau')
    plt.plot(epochs, metrics['ood_val_tau'], label='FashionMNIST OOD Val Tau')
    plt.plot(epochs, metrics['noisy_val_tau'], label='Noisy MNIST Val Tau')
    plt.title('Tau (Entropy) over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('Tau')
    plt.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'all_metrics_curves.png'))
    plt.close()


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])

    mnist_data_dir = "temp_data/MNIST"
    fashion_mnist_data_dir = "temp_data/FashionMNIST"
    output_dir = "output/"

    if not os.path.exists(mnist_data_dir):
        os.makedirs(mnist_data_dir)
    if not os.path.exists(fashion_mnist_data_dir):
        os.makedirs(fashion_mnist_data_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    train_dataset = datasets.MNIST(mnist_data_dir, train=True, download=True, transform=transform)
    val_dataset = datasets.MNIST(mnist_data_dir, train=False, download=True, transform=transform)
    ood_val_dataset = datasets.FashionMNIST(fashion_mnist_data_dir, train=False, download=True, transform=transform)

    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=1000, shuffle=False)
    ood_val_loader = DataLoader(ood_val_dataset, batch_size=1000, shuffle=False)

    noisy_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,)),
        AddGaussianNoise(0., 1.0) # Add Gaussian noise with mean 0 and std 1.0
    ])
    noisy_mnist_val_dataset = datasets.MNIST(mnist_data_dir, train=False, download=True, transform=noisy_transform)
    noisy_mnist_val_loader = DataLoader(noisy_mnist_val_dataset, batch_size=1000, shuffle=False)

    model = SimpleCNN().to(device)
    optimizer = optim.Adam(model.parameters())
    loss_fn = nn.CrossEntropyLoss()

    pi_monitor = PIMonitor(alpha=1.0, gamma=0.5)

    metrics = {
        'train_loss': [], 'train_acc': [], 'train_pi': [], 'train_surprise': [], 'train_tau': [],
        'val_loss': [], 'val_acc': [], 'val_pi': [], 'val_surprise': [], 'val_tau': [],
        'ood_val_loss': [], 'ood_val_acc': [], 'ood_val_pi': [], 'ood_val_surprise': [], 'ood_val_tau': [],
        'noisy_val_loss': [], 'noisy_val_acc': [], 'noisy_val_pi': [], 'noisy_val_surprise': [], 'noisy_val_tau': []
    }

    epochs = 5
    for epoch in range(1, epochs + 1):
        print(f"\n--- Epoch {epoch} ---")
        train_loss, train_acc, train_pi, train_surprise, train_tau = train(model, device, train_loader, optimizer, epoch, loss_fn, pi_monitor)
        val_loss, val_acc, val_pi, val_surprise, val_tau = validate(model, device, val_loader, loss_fn, pi_monitor, dataset_name="MNIST Validation")
        noisy_val_loss, noisy_val_acc, noisy_val_pi, noisy_val_surprise, noisy_val_tau = validate(model, device, noisy_mnist_val_loader, loss_fn, pi_monitor, dataset_name="Noisy MNIST Validation")
        ood_val_loss, ood_val_acc, ood_val_pi, ood_val_surprise, ood_val_tau = validate(model, device, ood_val_loader, loss_fn, pi_monitor, dataset_name="FashionMNIST OOD")

        metrics['train_loss'].append(train_loss)
        metrics['train_acc'].append(train_acc)
        metrics['train_pi'].append(train_pi)
        metrics['train_surprise'].append(train_surprise)
        metrics['train_tau'].append(train_tau)

        metrics['val_loss'].append(val_loss)
        metrics['val_acc'].append(val_acc)
        metrics['val_pi'].append(val_pi)
        metrics['val_surprise'].append(val_surprise)
        metrics['val_tau'].append(val_tau)

        metrics['ood_val_loss'].append(ood_val_loss)
        metrics['ood_val_acc'].append(ood_val_acc)
        metrics['ood_val_pi'].append(ood_val_pi)
        metrics['ood_val_surprise'].append(ood_val_surprise)
        metrics['ood_val_tau'].append(ood_val_tau)

        metrics['noisy_val_loss'].append(noisy_val_loss)
        metrics['noisy_val_acc'].append(noisy_val_acc)
        metrics['noisy_val_pi'].append(noisy_val_pi)
        metrics['noisy_val_surprise'].append(noisy_val_surprise)
        metrics['noisy_val_tau'].append(noisy_val_tau)

    plot_metrics(metrics, output_dir)
    print(f"\nPlots saved to: {os.path.abspath(output_dir)}")

if __name__ == "__main__":
    main()
