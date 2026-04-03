def hitung_produksi(total, pekerja, pekerja_sabtu, produktivitas):
    if pekerja < 0 or pekerja_sabtu < 0:
        raise ValueError("Jumlah pekerja tidak boleh negatif")

    weekly = pekerja * produktivitas * 5 + pekerja_sabtu * produktivitas
    
    if weekly == 0:
        return 0, 0, 0

    weeks = total / weekly
    years = weeks / 52

    return weekly, weeks, years


def kebutuhan_pekerja(total, target_tahun, produktivitas, hari):
    if target_tahun <= 0:
        raise ValueError("Target tahun harus > 0")

    weekly_target = total / (target_tahun * 52)
    pekerja = weekly_target / (produktivitas * hari)

    return pekerja


def cari_optimal(total, target_tahun, produktivitas, max_worker=100):
    for p in range(1, max_worker):
        for ps in range(0, p + 1):
            weekly = p * produktivitas * 5 + ps * produktivitas

            if weekly == 0:
                continue

            years = (total / weekly) / 52

            if years <= target_tahun:
                return p, ps, years

    return None