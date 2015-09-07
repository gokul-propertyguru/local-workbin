import pandas as pd
import os

def main():
    files = [{"fileName":"HDB_RENTALS_2012_2015","field_list":["id","building_number","postcode","hdb_id","hdb_estate"],"remove_field":["key_transaction","timestamp"]},
             {"fileName":"URA_RENTALS_2012_2015","field_list":["id","building_name","ura_key_id","postcode"],"remove_field":["id_job","timestamp"]},
             {"fileName":"HDB_SALES_2012_2015","field_list":["id","postcode","building_number","hdb_estate","hdb_estate_name","hdb_estate_code","hdb_id"],"remove_field":["key_transaction","timestamp"]},
             {"fileName":"URA_SALES_2012_2015","field_list":["id","ura_key","postcode","building_number","ura_key_id"],"remove_field":["bedrooms_stars","listing_ids","key_transaction","property_id_guru"]},
             {"fileName":"ENQUIRES_2014_2015","field_list":["user_id","listing_type","status_code","agent_id"],"remove_field":["id","property_id","screenname","property_type_code","region","remarks","title","contact_phone","contact_email"]},
             {"fileName":"LISTINGS_2014_2015","field_list":["postcode","agent_id","agency_id","property_type_group","source","account_type","hdb_estate"],"remove_field":["id", "sub_type_code", "price_description", "valuation_price", "description", "status_code", "extrarooms", "unit_description", "cover_image_id", "property_id", "streetname2", "agent_name", "agency", "agent_mobile_country", "agent_mobile", "agent_phone", "agent_email", "streetview_on_listings", "property_cover_image_id", "temporary_property_id", "alert_batch_id", "has_price", "has_size", "has_photos", "has_stream", "has_psf", "ad_code", "floorplan_id", "feature_code", "show_profile", "street_id", "moderation_status", "cobroke", "event_id", "completed_price", "corner_unit", "title_type", "occupancy", "facing", "refresh_left"]}
             ]
    path = os.getcwd()+os.sep+"working"+os.sep
    for f in files:
        df = pd.read_csv(path+f["fileName"]+".csv")
        field_list = f["field_list"]
        remove_field = f["remove_field"]
        mapper_dict = {}
        for field in remove_field:
            del df[field]
        cols = df.columns
        for field in field_list:
            field_vals = df[field]
            field_hash_pair = [[v,hash(str(v))] for v in field_vals]
            field_hash = [hash(str(v)) for v in field_vals]
            del df[field]
            df[field]=field_hash
            mapper_dict[field] = field_hash_pair
        rental_map = pd.DataFrame(mapper_dict)
        df = df[cols]
        rental_map.to_csv(path+"mapping"+os.sep+f["fileName"]+"_mapping.csv",index=False)
        df.to_csv(path+"hashed"+os.sep+f["fileName"]+"_hashed.csv",index=False)

if __name__=='__main__':
    main()