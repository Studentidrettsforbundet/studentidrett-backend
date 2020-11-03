import math

from questionnaire.models import Alternative
from questionnaire.serializers import AlternativeSerializer
from sports.models import Sport
from sports.serializers import SportSerializer


class RecommendationEngine:
    def __init__(self, request):
        self.request = request

    def get_weighting(self):
        # Counts how many answers correspond to each label and assigns a weight based on answer
        # Return a dictionary of label: weight
        result_dict = dict()
        weighting_dict = dict()
        for data in self.request.data:
            # Get the alternatives of the questions answered to process the numeric answer (0-4)
            alternatives = AlternativeSerializer(
                Alternative.objects.filter(qid=data["qid"]), many=True
            )
            ans = int(data.get("answer"))
            labels_list = []
            # Assuming that each question has 2 answers
            for x in range(0, 2):
                # Get all labels associated with the alternatives chosen
                labels = alternatives.data[x].get("labels")
                for label in labels:
                    labels_list.append(label.get("text"))
                    # Assign a weight to each label based on answer
                    # (0=(0,1), 1=(0.25, 0.75), 2=(0.5, 0.5) etc.)
                    # Assuming that labels of each alternative is distinct
                    weighting_dict[label.get("text")] = (
                        1 - (0.25 * ans) if x == 0 else 0.25 * ans
                    )
            # Iterate over labels and add weights to result-dictionary
            for label in labels_list:
                result_dict[label] = result_dict.get(label, 0) + weighting_dict.get(
                    label
                )
        return result_dict

    def distance_fn(self, features1, features2):
        # Simple Euclidean distance measure d(x1, x2)=sqrt(sum_i (x1_i - x2_i)^2))
        assert len(features1) == len(features2)
        total = 0
        for i in range(0, len(features1)):
            total += (features1[i] - features2[i]) ** 2
        return round(math.sqrt(total), 3)

    def calculate(self):
        sports_dict = dict()
        sports_id_dict = dict()
        answers = self.get_weighting()
        sports = Sport.objects.all()
        sport_list = SportSerializer(sports, many=True)
        labels = list(answers.keys())
        weights = list(answers.values())
        for sport in sport_list.data:
            sport_feats = [0 for _ in labels]
            sport_labels = [y.get("text") for y in (sport.get("labels"))]
            # Assign 0 or 1 depending on whether or not one of the labels
            # from answered questions exists on sport
            for i in range(0, len(labels)):
                if labels[i] in sport_labels:
                    sport_feats[i] = 1
            # Assign list of features to sport name
            sports_dict[sport.get("name")] = sport_feats
            sports_id_dict[sport.get("name")] = sport.get("id")
        results = []
        for key in sports_dict:
            obj = dict()
            obj["name"] = key
            obj["id"] = sports_id_dict[key]
            obj["score"] = self.distance_fn(sports_dict[key], weights)
            results.append(obj)
        return sorted(results, key=lambda x: x["score"])
