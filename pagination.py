import pickle as pkl
import json
import pdb

def create_html(json_data_python):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <link rel="stylesheet" href="tailwind.css" data-turbo-track="reload" />
    </head>

    <body onload="onLoad()">
      <main id="main_div" class="container mx-auto mt-14 px-5">
        <div class="md:grid md:grid-cols-3 md:gap-6 mt-12">
          <div class="md:col-span-1">
          </div>
          <div class="md:col-span-1">
          </div>
        </div>

        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="text-center mb-4">
            <p class="mt-1 text-4xl font-extrabold text-gray-900 sm:text-5xl sm:tracking-tight lg:text-6xl">Testing pagination</p>
          </div>
        </div>

        <div id="mygallery_div" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="text-center mb-4">
                <p class="mt-1 text-3xl font-extrabold text-gray-900 sm:text-3xl sm:tracking-tight lg:text-5xl">TEST PAGINATION</p>
          </div>
        </div>
      </main>

        <script type="text/javascript">
            // pass json object
            var json_data = {json_data_python};
            page = 0;
            first_time = true;

            function nextPage() {{
                page = page + 1;
                // delete the existing my gallery and next/prev links
                var el_p = document.getElementById("buttonsForChangePage");
                el_p.remove();

                var el = document.getElementById("actualMyGalleryDiv");
                el.remove();

                console.log("new page number " + page);
                onLoad();
                scroll(0,0);
            }}

            function onLoad() {{
                console.log("page loaded changing it");

                var myGallery = document.createElement("div");
                myGallery.className = "myGallery";
                myGallery.id = "actualMyGalleryDiv";
                // loop over first 10 items in the json data
                for (var i = 0; i < json_data[page].length; i++) {{
                    current_json_data = json_data[page][i];
                    // create inner html
                    item = document.createElement("div");
                    item.className = "item";

                    // subitem to store image and list of attributes
                    subitem = document.createElement("div");
                    subitem.className = "subitem";

                    // image div (for rarity)
                    var img_div = document.createElement("div");
                    img_div.className = "container mx-auto relative";

                    // image
                    var img = new Image();
                    img.src = current_json_data["cached_file_url"];
                    img_div.appendChild(img);

                    // rarity stuff
                    var rarity_div = document.createElement("div");
                    rarity_div.className = "bg-gradient-to-r opacity-95 from-yellow-200 to-yellow-500 w-24 h-1/8 absolute top-3 left-3 rounded-lg p-2 text-center text-slate-900 font-bold";
                    rarity_div.innerHTML = "Top " + current_json_data["rarity_percent"] +  "%";
                    img_div.appendChild(rarity_div)

                    subitem.appendChild(img_div);

                    // caption (contains the attributes)
                    var caption = document.createElement("span");
                    caption.className = "caption";

                    var ul = document.createElement("ul");
                    for (var key in current_json_data["attributes"]) {{
                        var li = document.createElement("li");
                        li.innerHTML = key + ": " + current_json_data["attributes"][key];
                        ul.appendChild(li);
                    }}
                    caption.appendChild(ul);
                    subitem.appendChild(caption);
                    item.appendChild(subitem);

                    // create div with the name and link
                    name_div = document.createElement("div");
                    name_div.className = "text-center mb-4";

                    // create link
                    var a = document.createElement("a");
                    a.target = "_blank";
                    a.href = "https://opensea.io/assets/" + current_json_data["contract"] + "/" + current_json_data["token_id"];
                    a.innerHTML = "Doodle #" + current_json_data["token_id"];

                    // create paragraph with link
                    p = document.createElement("p");
                    p.className = "underline text-xl text-blue-600 hover:text-blue-800";
                    p.appendChild(a);

                    name_div.appendChild(p);
                    item.appendChild(name_div);

                    myGallery.appendChild(item);
                }}

                mygallery_div = document.getElementById("mygallery_div");
                mygallery_div.appendChild(myGallery);

                // add pagination function
                main_div = document.getElementById("main_div");

                // buttons to go through list
                var buttons_div = document.createElement("div");
                buttons_div.id = "buttonsForChangePage";
                buttons_div.className = "flex justify-center items-center h-screen mb-4";


                var next_button_div = document.createElement("button");
                next_button_div.className = "bg-blue-400 hover:bg-blue-600 text-white text-lg font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded text-center";
                next_button_div.innerHTML = "Next";
                next_button_div.addEventListener('click', function(){{
                    nextPage();
                }});
                buttons_div.appendChild(next_button_div)

                main_div.appendChild(buttons_div);
                console.log("done");
            }}

        </script>

    </body>

    </html>
    """
    return html

if __name__ == "__main__":
    doodles_dict = pkl.load(open("doodles_very_small_info.pkl", "rb"))
    for d in doodles_dict:
        d["rarity_percent"] = min(max(1, int((d["rarity_index"] / len(doodles_dict)) * 100)), 99)

    num_items = 25

    doodles_dict_chunked = [doodles_dict[i:i + num_items] for i in range(0, len(doodles_dict), num_items)]

    doodles_json = json.dumps(doodles_dict_chunked)
    html = create_html(doodles_json)
    open("index_pagination.html", "w").write(html)
    print ("done")
