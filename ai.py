import random

from goscrape.database.models import Application


def set_categori_dict(apps):
    result = {}
    for i in apps:
        for j in i.categories:
            result[j.slug] = result.get(j.slug, 0) + 1
    return result


def set_training_list(apps):
    categori_dict = set_categori_dict(apps)
    training_list = []
    for i in apps:
        training_list.append([categori_dict.get(i.categories[0].slug, -1000),
                              i.size / 2.0 ** 20,
                              i.active_installs / 1000.0,
                              i.price / (1000.0 * -1),
                              i.rate, 1])
    return training_list, categori_dict


def update_weight(weight, targetOutput, output, learningrate, xi):
    TO = targetOutput - output
    for i in range(len(weight) - 1):
        deltaweight = learningrate * TO * xi[i]
        weight[i] += deltaweight
    return weight


def learn_ANN(training_list):
    weight = random.sample([i / 100.0 for i in range(100)], len(training_list[0]))
    learningrate = random.randrange(100) / 100.0
    i = 0
    while i < len(training_list):
        answer = weight[-1]
        print 'weight ', weight
        for j in range(len(training_list[i]) - 1):
            answer += training_list[i][j] * weight[j]
        print 'answer ', answer
        if answer / 10000.0 > 1:
            answer = 1
        else:
            answer = -1
        if training_list[i][-1] != answer:
            update_weight(weight, training_list[i][-1], answer, learningrate, training_list[i])
            i = 0
        else:
            i += 1
    return weight


def set_answer(app, weight, categori_dict):
    return weight[0] * categori_dict.get(app.categories[0].slug, -1000) + \
           weight[1] * app.size / 2.0 ** 20 + \
           weight[2] * app.active_installs / 1000.0 + \
           weight[3] * app.price / (1000.0 * -1) + \
           weight[4] * app.rate + \
           weight[5]


def get_suggested_apps(apps):
    training_list, categori_dict = set_training_list(apps)
    weight = learn_ANN(training_list)
    result = []
    print weight
    print categori_dict
    for i in Application.query.all():
        if categori_dict.get(i.categories[0].slug, 0) == 0:
            continue
        answer = set_answer(i, weight, categori_dict)
        # print 'finall answer : ', answer
        if answer / 10000.0 > 1:
            # print answer
            result.append((i, answer))
    print len(result)
    result.sort(key=lambda x: x[1], reverse=True)
    return [i[0] for i in result[:20]]
