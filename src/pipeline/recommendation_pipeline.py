from src.components.recommendation_builder import BuildRecommendation

if __name__ == "__main__":
    obj = BuildRecommendation()
    data = obj.initiate_data_ingestion()
    model = obj.build_recommendation(data)
    obj.initiate_recommendation("Grand Village",data,model)