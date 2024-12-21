from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Ganti dengan kunci rahasia Anda

# Deklarasi variabel global
akun1 = "Daffa Tari Saman"
pin1 = 111000
saldo = 50000000  # Saldo awal
rek1 = 2210171040  # Nomor rekening
akunATM = None

@app.route("/", methods=["GET", "POST"])
def welcome():
    global akunATM
    if request.method == "POST":
        inputPin = request.form.get("pin", type=int)
        return verifikasi(inputPin)  # Memanggil fungsi verifikasi
    return render_template("welcome.html")  # Tampilkan halaman sambutan

def verifikasi(p):
    global akunATM
    if p == pin1:
        akunATM = akun1  # Menyimpan nama akun
        return redirect(url_for("menu"))  # Arahkan ke menu
    else:
        flash("PIN salah! Silakan coba lagi.")
        return redirect(url_for("welcome"))  # Kembali ke tampilan awal jika PIN salah

@app.route("/menu", methods=["GET", "POST"])
def menu():
    if request.method == "POST":
        pilihan = request.form.get("pilihan", type=int)
        if pilihan == 1:
            return redirect(url_for("cekSaldo"))
        elif pilihan == 2:
            return redirect(url_for("tarikTunai"))
        elif pilihan == 3:
            return redirect(url_for("transfer"))
        elif pilihan == 4:
            return redirect(url_for("welcome"))
        else:
            flash("Pilihan tidak valid. Silakan coba lagi.")
            return redirect(url_for("menu"))

    return render_template("menu.html",akun1=akun1,rek1=rek1)  # Tampilkan menu

@app.route("/cek_saldo")
def cekSaldo():
    return render_template("cek_saldo.html", saldo=saldo,akun1=akun1,rek1=rek1)  # Tampilkan saldo

@app.route("/tarik_tunai", methods=["GET", "POST"])
def tarikTunai():
    global saldo
    if request.method == "POST":
        jumlah = request.form.get("jumlah", type=int)
        if jumlah > saldo:
            flash("Saldo tidak cukup!")
        else:
            saldo -= jumlah  # Mengurangi saldo
            flash(f"Anda telah menarik: {jumlah}. Saldo Anda sekarang: {saldo}")
        return redirect(url_for("menu"))
    return render_template("tarik_tunai.html",akun1=akun1,rek1=rek1)  # Tampilkan halaman tarik tunai

@app.route("/transfer", methods=["GET", "POST"])
def transfer():
    global saldo
    if request.method == "POST":
        jumlah = request.form.get("jumlah", type=int)
        if jumlah > saldo:
            flash("Saldo tidak cukup untuk transfer!")
        else:
            saldo -= jumlah  # Mengurangi saldo
            flash(f"Anda telah mentransfer: {jumlah}. Saldo Anda sekarang: {saldo}")
        return redirect(url_for("menu"))
    return render_template("transfer.html",akun1=akun1,rek1=rek1)  # Tampilkan halaman transfer

if __name__ == "__main__":
    app.run(debug=True)