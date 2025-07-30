import torch

class Node:
    def __init__(self, input_size, output_size, init_type, scale, device):
        if init_type == 'he':
            stddev = torch.sqrt(torch.tensor(2 / input_size, device=device))
        elif init_type == 'xavier':
            stddev = torch.sqrt(torch.tensor(1 / input_size, device=device))
        else:
            stddev = scale
        self.w = torch.normal(0, stddev, (input_size, output_size), device=device)
        self.b = torch.zeros(1, output_size, device=device)


def Identity(X, device='cpu'):
    if not isinstance(X, torch.Tensor):
        raise ValueError("Error: X must be a torch.Tensor.")
    X = (X.float()).to(device)
    return X

def Tanh(X, device='cpu'):
    if not isinstance(X, torch.Tensor):
        raise ValueError("Error: X must be a torch.Tensor.")
    X = (X.float()).to(device)
    return (torch.exp(X) - torch.exp(-X)) / (torch.exp(X) + torch.exp(-X))

def Sigmoid(X, device='cpu'):
    if not isinstance(X, torch.Tensor):
        raise ValueError("Error: X must be a torch.Tensor.")
    X = (X.float()).to(device)
    return 1 / (1 + torch.exp(-X))

def ReLU(X, device='cpu'):
    if not isinstance(X, torch.Tensor):
        raise ValueError("Error: X must be a torch.Tensor.")
    X = (X.float()).to(device)
    return torch.maximum(torch.tensor(0.0, device=device), X)

def LeakyReLU(X, device='cpu', alpha=0.01):
    if not isinstance(X, torch.Tensor):
        raise ValueError("Error: X must be a torch.Tensor.")
    X = (X.float()).to(device)
    return torch.where(X > 0, X, alpha * X)

def GELU(X, device='cpu'):
    if not isinstance(X, torch.Tensor):
        raise ValueError("Error: X must be a torch.Tensor.")
    X = (X.float()).to(device)
    return 0.5 * X * (1 + torch.tanh(torch.sqrt(torch.tensor(2 / torch.pi, device=device)) * (X + 0.044715 * torch.pow(X, 3))))

def Swish(X, device='cpu'):
    if not isinstance(X, torch.Tensor):
        raise ValueError("Error: X must be a torch.Tensor.")
    X = (X.float()).to(device)
    return X * (1 / (1 + torch.exp(-X)))

def Softmax(X, device='cpu'):
    if not isinstance(X, torch.Tensor):
        raise ValueError("Error: X must be a torch.Tensor.")
    X = (X.float()).to(device)
    e_x = torch.exp(X - torch.max(X))
    return e_x / e_x.sum()

def BinaryStep(X, device='cpu'):
    if not isinstance(X, torch.Tensor):
        raise ValueError("Error: X must be a torch.Tensor.")
    X = (X.float()).to(device)
    return (X > 0).int()



def CrossEntropy(X, Y, device='cpu'):
    if not isinstance(X, torch.Tensor) or not isinstance(Y, torch.Tensor):
        raise ValueError("Error: X and Y must be a torch.Tensor.")
    X = (X.float()).to(device)
    Y = (Y.float()).to(device)
    import torch.nn.functional as F
    return F.cross_entropy(X, Y.to(torch.long).to(device))

def MeanSquaredError(X, Y, device='cpu'):
    if not isinstance(X, torch.Tensor) or not isinstance(Y, torch.Tensor):
        raise ValueError("Error: X and Y must be a torch.Tensor.")
    X = (X.float()).to(device)
    Y = (Y.float()).to(device)
    return torch.mean((Y - X)**2)

def MeanAbsoluteError(X, Y, device='cpu'):
    if not isinstance(X, torch.Tensor) or not isinstance(Y, torch.Tensor):
        raise ValueError("Error: X and Y must be a torch.Tensor.")
    X = (X.float()).to(device)
    Y = (Y.float()).to(device)
    return torch.mean(torch.abs((Y - X)))

def CrossCategoricalEntropy(X, Y, device='cpu'):
    if not isinstance(X, torch.Tensor) or not isinstance(Y, torch.Tensor):
        raise ValueError("X and Y must be torch.Tensor.")
    X = X.float().to(device)
    Y = Y.float().to(device)
    import torch.nn.functional as F
    log_probs = F.log_softmax(X, dim=1)
    loss = -torch.sum(Y * log_probs, dim=1)
    return torch.mean(loss)

def BinaryCrossEntropy(X, Y, device='cpu'):
    if not isinstance(X, torch.Tensor) or not isinstance(Y, torch.Tensor):
        raise ValueError("X and Y must be torch.Tensor.")
    X = X.float().to(device)
    Y = Y.float().to(device)
    X = torch.clamp(X, 1e-7, 1 - 1e-7)
    loss = -(Y * torch.log(X) + (1 - Y) * torch.log(1 - X))
    return torch.mean(loss)

def KullbackLeiblerDivergence(X, Y, device='cpu'):
    if not isinstance(X, torch.Tensor) or not isinstance(Y, torch.Tensor):
        raise ValueError("X and Y must be torch.Tensor.")
    X = torch.clamp(X, 1e-7, 1.0)
    Y = torch.clamp(Y, 1e-7, 1.0)
    X = X.float().to(device)
    Y = Y.float().to(device)
    return torch.mean(torch.sum(Y * (torch.log(Y) - torch.log(X)), dim=1))

def CosineLoss(X, Y, device='cpu'):
    if not isinstance(X, torch.Tensor) or not isinstance(Y, torch.Tensor):
        raise ValueError("X and Y must be torch.Tensor.")
    X = X.float().to(device)
    Y = Y.float().to(device)
    return 1 - torch.nn.functional.cosine_similarity(X, Y).mean()

def Accuracy(X, Y, device='cpu'):
    if not isinstance(X, torch.Tensor) or not isinstance(Y, torch.Tensor):
        raise ValueError("X and Y must be torch.Tensor.")
    X = X.float().to(device)
    Y = Y.float().to(device)
    X = X.argmax(dim=1)
    Y = Y.argmax(dim=1)
    return (X == Y).float().mean().item()





class Genoa:
    def __init__(self, layer_size, device='cpu', init_type='he', scale=2):
        self.device = device
        self.layer_size = layer_size
        self.mutate_fn = self.mutate
        self.loss_fn = MeanSquaredError
        self.hidden_fn = LeakyReLU
        self.output_fn = Sigmoid
        self.metric = Accuracy
        self.loss_history = []

        if len(self.layer_size) < 2:
            raise ValueError('Error: Expected at least 2 layers (input and output).')
        
        if self.device not in ['cuda', 'cpu']:
            raise ValueError('Error: Device must be cuda (for gpu) or cpu.')
        
        if self.hidden_fn is None or self.output_fn is None or self.loss_fn is None or self.mutate_fn is None:
            raise ValueError('hidden_fn, output_fn, mutate_fn, and loss_fn must be valid functions.')

        self.layers = []
        for i in range(1, len(layer_size)):
            self.layers.append(Node(layer_size[i-1], layer_size[i], init_type, scale, device))

    def mutate(self, X, mr):
        return X + torch.normal(0, mr, X.shape, device=self.device)

    def train(self, X, Y, mr=0.1, dr=0.999, generations=1000, population=50, batch_size=None, progress_style='tqdm', early_stop=None, optim_mr=False, threshold=50):
        if not isinstance(X, torch.Tensor) or not isinstance(Y, torch.Tensor):
            raise ValueError("X and Y must be a torch.Tensor.")
        X = (X.float()).to(self.device)
        Y = (Y.float()).to(self.device)
        
        x_batch = X
        y_batch = Y

        best = [float('inf'), None, None]
        prev_loss = float('inf')

        n = 0

        if batch_size and (not isinstance(batch_size, int) or batch_size <= 0):
            raise ValueError(f"Error: batch_size must be either >= 1 or None.")

        if progress_style not in ['tqdm', 'rich', 'halo']:
            raise ValueError(f"Error: progress_style must be tqdm, rich or halo.")

        if population < 2 or generations < 0:
            raise ValueError("Error: Training not possible. Population must be >=2 and generations >=1.")
        else:
            progress = None
            spinner = None
            desc = 'Training'
            if progress_style == 'tqdm':
                from tqdm import tqdm
                progress = tqdm(range(generations), desc=(desc+': '))
            elif progress_style == 'rich':
                from rich.progress import track
                progress = track(range(generations), description=(desc+': '))
            elif progress_style == 'halo':
                from halo import Halo
                spinner = Halo(text=(desc+'...'))
                spinner.start()

            try:
                for gen in (progress if progress else range(generations)):
                    if isinstance(batch_size, int) and 1 <= batch_size < len(X):
                        idx = torch.randperm(len(X))[:batch_size]
                        x_batch = X[idx]
                        y_batch = Y[idx]
                    
                    losses = []
                    for _ in range(population):
                        weights = []
                        biases = []

                        for i in range(len(self.layers)):
                            w = self.mutate_fn(self.layers[i].w, mr)
                            b = self.mutate_fn(self.layers[i].b, mr)
                            weights.append(w)
                            biases.append(b)
                        
                        h = x_batch
                        for i in range(len(self.layers)):
                            h = self.calc(h, weights[i], biases[i], self.layers[i])

                        losses.append([self.loss_fn(h, y_batch, device=self.device), weights, biases])
                        
                    p1, p2 = sorted(losses, key=lambda x: x[0])[:2]

                    if best[0] > p1[0]:
                        best = p1

                    self.loss_history.append(best[0])

                    for i in range(len(self.layers)):
                        self.layers[i].w = ((p1[1])[i] + 0.5*((p2[1])[i]))/1.5
                        self.layers[i].b = ((p1[2])[i] + 0.5*((p2[2])[i]))/1.5

                    loss = self.loss_fn(self.forward(x_batch), y_batch, device=self.device)

                    if early_stop != None and loss <= early_stop:
                        print(f"Loss reached {early_stop}. Training stopped...")
                        break
                    
                    if optim_mr:
                        if prev_loss > loss:
                            mr *= dr
                            n = 0
                        else:
                            n += 1
                            if n >= threshold:
                                mr += mr*(1-dr)*dr
                                n = 0
                    else:
                        mr *= dr

                    mr = max(0, min(0.5, mr))

                    prev_loss = loss

                    if loss <= p2[0]:
                        if loss <= p1[0]:
                            for i in range(len(self.layers)):
                                self.layers[i].w = (0.5*((p1[1])[i])+self.layers[i].w)/1.5
                                self.layers[i].b = (0.5*((p1[2])[i])+self.layers[i].b)/1.5
                        else:
                            for i in range(len(self.layers)):
                                self.layers[i].w = ((p1[1])[i]+(0.5*(self.layers[i].w)))/1.5
                                self.layers[i].b = ((p1[2])[i]+(0.5*(self.layers[i].b)))/1.5
                    else:
                        for i in range(len(self.layers)):
                            self.layers[i].w = ((p1[1])[i]+(0.5*(p2[1])[i]))/1.5
                            self.layers[i].b = ((p1[2])[i]+(0.5*(p2[2])[i]))/1.5
                
                loss = self.loss_fn(self.forward(x_batch), y_batch, device=self.device)
                if loss > best[0]:
                    for i in range(len(self.layers)):
                        self.layers[i].w = best[1][i]
                        self.layers[i].b = best[2][i]
            except Exception as e:
                import traceback
                print(f"[Error at {gen}]: {e}")
                traceback.print_exc()
            finally:
                if spinner:
                    spinner.succeed('Training Complete.')

    def calc(self, X, W, B, layer):
        if not isinstance(X, torch.Tensor):
            raise ValueError("Error: X must be a torch.Tensor.")
        X = (X.float()).to(self.device)
        X = torch.addmm(B, X, W)
        if layer == self.layers[-1]:
            return self.output_fn(X)
        else:
            return self.hidden_fn(X)

    def forward(self, X):
        if not isinstance(X, torch.Tensor):
            raise ValueError("Error: X must be a torch.Tensor.")
        X = (X.float()).to(self.device)
        for i in range(len(self.layers)):
            X = self.calc(X, self.layers[i].w, self.layers[i].b, self.layers[i])
        return X

    def save(self, file_name='model'):
        model_data = {
            'layer_size' : self.layer_size,
            'layers' : self.layers,
            'loss_fn' : self.loss_fn,
            'hidden_fn' : self.hidden_fn,
            'output_fn' : self.output_fn,
            'metric' : self.metric,
            'weights' : {f'w{i}': layer.w.cpu() for i, layer in enumerate(self.layers)},
            'biases' : {f'b{i}': layer.b.cpu() for i, layer in enumerate(self.layers)}
        }
        torch.save(model_data, file_name + '.pt')

    @classmethod
    def load(cls, file_name='model', device='cpu'):
        data = torch.load(file_name + '.pt', map_location=device, weights_only=False)

        model = cls(data['layer_size'], device=device)

        model.layers = data['layers']
        model.loss_fn = data['loss_fn']
        model.hidden_fn = data['hidden_fn']
        model.output_fn = data['output_fn']

        for layer in model.layers:
            layer.w = layer.w.to(device)
            layer.b = layer.b.to(device)
        
        return model

    def graph(self):
        if hasattr(self, "loss_history"):
            loss_history = [loss.item() if isinstance(loss, torch.Tensor) else loss for loss in self.loss_history]

            import matplotlib.pyplot as plt
            plt.figure(figsize=(10, 4))
            plt.plot(loss_history, label="Loss", color="blue")
            plt.xlabel("Generation")
            plt.ylabel("Loss")
            plt.title("GENOA Training Progress")
            plt.grid(True)
            plt.legend()
            plt.tight_layout()
            plt.show()
        else:
            print("No training history found. Run `train()` first.")




# class EvoNet:
#     def __init__(self, models: list, fitness_scores: list, population_size: int = None):
#         self.models = models
#         self.fitness_scores = fitness_scores
#         self.population_size = population_size

#     def evolve(self, mr=0.5):
#         performance = sorted(
#             zip(self.fitness_scores, self.models),
#             key=lambda x: x[0],
#             reverse=True
#         )

#         h1 = self.tournament()
#         h2 = self.tournament()

#         new_population = [h1, h2]

#         p = (self.population_size//2) - 2

#         for i in range(p):
#             model = Genoa(h1.layer_size.copy())
#             for layer in model.layers:
#                 layer.w = model.mutate_fn(layer.w, mr)
#                 layer.b = model.mutate_fn(layer.b, mr)
            
#             new_population.append(model)
        
#         while len(new_population) < self.population_size:
#             layer_size = h1.layer_size.copy()

#             if random.random() < 0.5:
#                 layer_size = self.add_layer(layer_size)
#             else:
#                 layer_size = self.add_node(layer_size)

#             model = Genoa(layer_size)
#             new_population.append(model)

#         return new_population

#     def add_node(self, layer_size):
#         layer_size = layer_size.copy()

#         if len(layer_size) > 2:
#             layer = random.randint(1, len(layer_size) - 2)
#             layer_size[layer] += 1
        
#         return layer_size

#     def add_layer(self, layer_size):
#         layer_size = layer_size.copy()
#         layer = len(layer_size) - 1

#         layer_size.insert(layer, 1)

#         return layer_size

#     def tournament(self, k=3):
#         competitors = random.sample(list(zip(self.fitness_scores, self.models)), k)
#         competitors.sort(key=lambda x: x[0], reverse=True)
#         return competitors[0][1]  # Return the best model among them