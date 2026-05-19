import 'package:path/path.dart' as p;
import 'package:path_provider/path_provider.dart';
import 'package:sqflite/sqflite.dart';

import '../models.dart';

class StorageService {
  Database? _database;

  Future<Database> get database async {
    if (_database != null) {
      return _database!;
    }
    final dir = await getApplicationDocumentsDirectory();
    final dbPath = p.join(dir.path, 'coral_health_ai.db');
    _database = await openDatabase(
      dbPath,
      version: 1,
      onCreate: (db, version) async {
        await db.execute('''
          CREATE TABLE history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prediction TEXT NOT NULL,
            confidence REAL NOT NULL,
            image_path TEXT NOT NULL,
            created_at TEXT NOT NULL,
            model_mode TEXT NOT NULL,
            probabilities_json TEXT NOT NULL,
            status_json TEXT NOT NULL,
            model_used TEXT NOT NULL,
            original_image TEXT NOT NULL,
            overlay_image TEXT NOT NULL,
            heatmap_image TEXT NOT NULL,
            uncertainty INTEGER NOT NULL DEFAULT 0
          )
        ''');
        await db.execute('''
          CREATE TABLE settings(
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
          )
        ''');
      },
    );
    return _database!;
  }

  Future<List<HistoryEntry>> loadHistory() async {
    final db = await database;
    final rows = await db.query('history', orderBy: 'created_at DESC');
    return rows.map(HistoryEntry.fromMap).toList();
  }

  Future<void> saveHistoryEntry(HistoryEntry entry) async {
    final db = await database;
    final values = entry.toMap()..remove('id');
    await db.insert(
      'history',
      values,
      conflictAlgorithm: ConflictAlgorithm.replace,
    );
  }

  Future<void> deleteHistoryEntry(int id) async {
    final db = await database;
    await db.delete('history', where: 'id = ?', whereArgs: [id]);
  }

  Future<void> saveSetting(String key, String value) async {
    final db = await database;
    await db.insert('settings', {
      'key': key,
      'value': value,
    }, conflictAlgorithm: ConflictAlgorithm.replace);
  }

  Future<String?> getSetting(String key) async {
    final db = await database;
    final rows = await db.query(
      'settings',
      where: 'key = ?',
      whereArgs: [key],
      limit: 1,
    );
    if (rows.isEmpty) {
      return null;
    }
    return rows.first['value'] as String?;
  }
}
