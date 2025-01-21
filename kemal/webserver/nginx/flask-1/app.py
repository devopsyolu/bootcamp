from flask import Flask, request, jsonify

app = Flask(__name__)

# Basit bir "Merhaba Dünya" rotası
@app.route("/", methods=["GET"])
def hello():
    return "Merhaba! Bu daha gelişmiş bir Flask uygulaması. App1"

# Hafifçe simule edilmiş bir bellek içi 'veritabanı' örneği
items_db = [
    {"id": 1, "name": "Laptop", "price": 1500},
    {"id": 2, "name": "Mouse",  "price": 20},
]

# 1) Tüm eşyaları listeleme (GET /items)
@app.route("/items", methods=["GET"])
def list_items():
    """
    Tüm eşyaları JSON formatında döndürür.
    """
    return jsonify(items_db), 200

# 2) Yeni eşya oluşturma (POST /items)
@app.route("/items", methods=["POST"])
def create_item():
    """
    Gövdesinde (body) "name" ve "price" göndermeniz beklenir.
    Örnek JSON: {"name": "Keyboard", "price": 40}
    """
    data = request.get_json()
    if not data or "name" not in data or "price" not in data:
        return jsonify({"error": "Eksik veya geçersiz veri"}), 400

    # Yeni id için basit bir yaklaşım: en yüksek id'yi bulup 1 eklemek
    new_id = max(item["id"] for item in items_db) + 1 if items_db else 1
    new_item = {
        "id": new_id,
        "name": data["name"],
        "price": data["price"]
    }
    items_db.append(new_item)
    return jsonify(new_item), 201

# 3) Tek bir eşyayı görüntüleme (GET /items/<id>)
@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    """
    Parametrede verilen ID'ye sahip eşyayı döndürür.
    """
    item = next((i for i in items_db if i["id"] == item_id), None)
    if item is None:
        return jsonify({"error": "Eşya bulunamadı"}), 404
    return jsonify(item), 200

# 4) Tek bir eşyayı güncelleme (PUT /items/<id>)
@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    """
    Gövdesinde (body) "name" ve/veya "price" göndermeniz beklenir.
    Örnek JSON: {"name": "Wireless Mouse", "price": 25}
    """
    data = request.get_json()
    item = next((i for i in items_db if i["id"] == item_id), None)
    if item is None:
        return jsonify({"error": "Güncellenecek eşya bulunamadı"}), 404

    # Güncellenecek alanlar
    item["name"] = data.get("name", item["name"])
    item["price"] = data.get("price", item["price"])
    return jsonify(item), 200

# 5) Tek bir eşyayı silme (DELETE /items/<id>)
@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    """
    Parametrede verilen ID'ye sahip eşyayı siler.
    """
    global items_db
    item = next((i for i in items_db if i["id"] == item_id), None)
    if item is None:
        return jsonify({"error": "Silinecek eşya bulunamadı"}), 404

    items_db = [i for i in items_db if i["id"] != item_id]
    return "", 204
# 6) Çalışan portu gösteren /app1 rotası
@app.route("/app1", methods=["GET"])
def show_port():
    """
    Çalışan portu döndüren rota.
    """
    port = request.environ.get("SERVER_PORT")
    return jsonify({"port": port})
# 7) 500 dondurme
@app.route("/manual-error", methods=["GET"])
def manual_error():
    return "", 500



if __name__ == "__main__":
    # Flask varsayılan olarak 5000 portunda çalışır
    # host='0.0.0.0' => Her IP arayüzünden gelen istekleri kabul etmek için
    app.run(host="0.0.0.0", port=5000, debug=True)