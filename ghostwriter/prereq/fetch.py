from docx import Document


class Fetch:
    def fetch_fun():
        wordDoc = Document("ghostwriter/prereq/Security Assessment Pre.docx")

        dict = {
            "Asset Name": "",
            "Asset Owner": "",
            "OS Type": "",
            "Application Name": "",
            "Stream": "",
            "Cluster": "",
            "Stream Head": "",
            "Cluster Head": "",
            "Service Category": "",
            "Business Owner Group": "",
            "Business Owner Unit": "",
            "Server Owner": "",
            "IT Owner": "",
            "IT Coordinator during Security Review": "",
            "Location": "",
        }

        result = ""

        for row in wordDoc.tables[-1].rows:
            for cell in row.cells:
                result = result + cell.text + "\n"

        result = result.split("\n")

        for i in result:
            if i in dict:
                dict[i] = result[result.index(i) + 1]

        final_dict = {
            "stream": dict["Stream"],
            "stream_head": dict["Stream Head"],
            "cluster": dict["Cluster"],
            "cluster_head": dict["Cluster Head"],
            "application_owner": dict["Asset Owner"],
            "business_group": dict["Business Owner Group"],
            "business_unit": dict["Business Owner Unit"],
            "business_owner": dict["Server Owner"],
            "it_owner": dict["IT Owner"],
            "development_team": dict["Location"],
        }

        return final_dict
