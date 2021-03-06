package tech.cuda.models

import org.jetbrains.exposed.sql.Database
import org.jetbrains.exposed.sql.transactions.transaction
import org.jetbrains.exposed.sql.SchemaUtils

/**
 * Created by Jensen on 18-6-19.
 */

val tables = listOf(GroupTable, InstanceTable, JobTable, MachineTable, ActionTable, TaskTable, UserTable)

fun getDatabase(): Database {
    return Database.connect(
            user = "root",
            password = "qijinxiu",
            url = "jdbc:mysql://localhost/chin",
            driver = "com.mysql.jdbc.Driver"
    )
}

fun createTables() {
    val db = getDatabase()
    transaction(db) {
        SchemaUtils.create(GroupTable, InstanceTable, JobTable, MachineTable, ActionTable, TaskTable, UserTable)
    }
}

fun dropTables() {
    val db = getDatabase()
    transaction(db) {
        SchemaUtils.drop(GroupTable, InstanceTable, JobTable, MachineTable, ActionTable, TaskTable, UserTable)
    }
}

fun rebuildTables() {
    dropTables()
    createTables()
}

