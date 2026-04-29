import 'package:flutter/material.dart';
import 'services/api_service.dart';
import 'models/estacion.dart';

void main() => runApp(const SMATApp());

class SMATApp extends StatelessWidget {
  const SMATApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  List<Estacion> estaciones = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    cargarEstaciones();
  }

  Future<void> cargarEstaciones() async {
    try {
      final data = await ApiService().fetchEstaciones();

      setState(() {
        estaciones = data;
        loading = false;
      });
    } catch (e) {
      setState(() {
        loading = false;
      });

      debugPrint("Error cargando estaciones: $e");
    }
  }

  Future<void> refrescar() async {
    setState(() {
      loading = true;
    });

    await cargarEstaciones();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('SMAT - Monitoreo Móvil'),
      ),

      body: loading
          ? const Center(child: CircularProgressIndicator())
          : estaciones.isEmpty
              ? const Center(
                  child: Text("No hay estaciones registradas"),
                )
              : ListView.builder(
                  itemCount: estaciones.length,
                  itemBuilder: (context, index) {
                    final est = estaciones[index];

                    return ListTile(
                      leading: const Icon(Icons.satellite_alt),
                      title: Text(est.nombre),
                      subtitle: Text(est.ubicacion),
                    );
                  },
                ),

      floatingActionButton: FloatingActionButton(
        onPressed: refrescar,
        child: const Icon(Icons.refresh),
      ),
    );
  }
}