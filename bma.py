import numpy as np
import torch

def threshold_loss(Y_reference, Y_model, threshold):
    cost = ((Y_reference[Y_reference>threshold]-Y_model[Y_reference>threshold])**2).mean()
    return cost

def bma(data, models: list, reference: str):
    '''
    Bayesian model averaging with loss = 
    '''
    y_T = torch.tensor(data[reference])
    
    m=[]
    for i, model in enumerate(models):
        m.append(torch.tensor(data[model]).reshape(-1,1))
        
    m_k = torch.cat(m, axis=1)
    n_m = m_k.shape[1]

    log_s = torch.nn.Parameter(torch.ones(n_m))
    log_w = torch.nn.Parameter(torch.ones(n_m))
        
    softmax = torch.nn.Softmax(dim=0)
    optimizer = torch.optim.Adam([log_s, log_w], lr=0.01)
    
    for i in range(500):
        optimizer.zero_grad()
        w = softmax(log_w)
        mixture_distribution = torch.distributions.Categorical(logits=log_w)
        component_distribution = torch.distributions.Normal(m_k, log_s.exp())
        gmm = torch.distributions.MixtureSameFamily(mixture_distribution, component_distribution)
        log_post = gmm.log_prob(y_T).sum() + torch.distributions.Dirichlet(torch.ones(n_m)).log_prob(w)
        loss = -log_post
        loss.backward()
        optimizer.step()
    return w

        
def bma_threshold(data, models: list, reference, threshold):
    
    y_T = torch.tensor(data[reference])
    
    m=[]
    for i, model in enumerate(models):
        m.append(torch.tensor(data[model]).reshape(-1,1))
        
    m_k = torch.cat(m, axis=1)
    n_m = m_k.shape[1]

    log_s = torch.nn.Parameter(torch.ones(n_m))
    log_w = torch.nn.Parameter(torch.ones(n_m))
        
    softmax = torch.nn.Softmax(dim=0)
    optimizer = torch.optim.Adam([log_s, log_w], lr=0.01)
    #loss_plot = []
    
    for i in range(500):
        optimizer.zero_grad()
        w = softmax(log_w)
        mixture_distribution = torch.distributions.Categorical(logits=log_w)
        component_distribution = torch.distributions.Normal(m_k, log_s.exp())
        gmm = torch.distributions.MixtureSameFamily(mixture_distribution, component_distribution)
        y_predicted=(w*m_k).sum(axis=1)
        loss = threshold_loss(y_T, y_predicted, threshold)
        loss.backward()
        optimizer.step()
        

    return w