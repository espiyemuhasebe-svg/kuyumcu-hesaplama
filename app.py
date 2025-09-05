from flask import Flask, render_template_string, request

app = Flask(__name__)

# Bootstrap ile şık HTML
html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Kuyumcu Hesaplama</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body class="bg-light">
<div class="container mt-5">
    <div class="card shadow-lg p-4">
        <h2 class="text-center text-primary">Kuyumcu Hesaplama</h2>
        <form method="POST">
            <table class="table table-bordered mt-3">
                <thead class="table-secondary">
                    <tr>
                        <th>Gram</th>
                        <th>Satış Fiyatı</th>
                        <th>Borsa Fiyatı</th>
                    </tr>
                </thead>
                <tbody>
                {% for i in range(5) %}
                    <tr>
                        <td><input type="number" step="0.01" name="gram{{i}}" class="form-control"></td>
                        <td><input type="number" step="0.01" name="satis{{i}}" class="form-control"></td>
                        <td><input type="number" step="0.01" name="borsa{{i}}" class="form-control"></td>
                    </tr>
                {% endfor %}
                </tbody>
            </table>
            <div class="text-center">
                <button type="submit" class="btn btn-primary">Hesapla</button>
            </div>
        </form>

        {% if sonuc %}
        <div class="alert alert-info mt-4">
            <h5>Sonuçlar</h5>
            <pre>{{ sonuc }}</pre>
        </div>
        {% endif %}
    </div>
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    sonuc = None
    if request.method == "POST":
        gramlar, satis_fiyatlari, borsa_fiyatlari = [], [], []

        for i in range(5):
            g = float(request.form.get(f"gram{i}", 0) or 0)
            s = float(request.form.get(f"satis{i}", 0) or 0)
            b = float(request.form.get(f"borsa{i}", 0) or 0)
            gramlar.append(g)
            satis_fiyatlari.append(s)
            borsa_fiyatlari.append(b)

        toplam_satis = sum(gramlar[i] * satis_fiyatlari[i] for i in range(len(gramlar)))
        toplam_borsa = sum(gramlar[i] * borsa_fiyatlari[i] for i in range(len(gramlar)))
        net_kar = (toplam_satis - toplam_borsa) / 1.2 if toplam_satis > 0 else 0
        KDV = net_kar * 20 / 100

        sonuc = (
            f"Toplam Satış: {toplam_satis:,.2f} ₺\\-"
            f"Toplam Borsa: {toplam_borsa:,.2f} ₺\\-"
            f"Net Kar: {net_kar:,.2f} ₺\\-"
            f"Kdv (%20): {kdv:,.2f} ₺"
        )

    return render_template_string(html, sonuc=sonuc)

if __name__ == "__main__":
    app.run(debug=True)



